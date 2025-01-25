"""Session auth controller."""
from typing import Callable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.session_auth import LoginRequest, SessionCookieConfig
from app.application.use_cases.auth.login_session.login import LoginUseCase
from app.application.use_cases.auth.login_session.logout import LogoutUseCase
from app.domain.entities.login_session import LoginSession
from app.domain.repositories.login_session import LoginSessionRepository
from app.domain.repositories.user import UserByEmailRepository
from app.domain.services.auth.base import UserAuthService
from app.domain.services.auth.login_session import LoginSessionService
from app.interfaces.controllers.v1.path import AUTH_SESSION_PREFIX, \
    SESSION_LOGIN_ENDPOINT
from app.interfaces.middlewares.auth_middleware import get_session

router = APIRouter(
    prefix=AUTH_SESSION_PREFIX,
    tags=['auth-session'],
)


# pylint: disable=too-many-arguments,too-many-positional-arguments
@router.post(SESSION_LOGIN_ENDPOINT)
@inject
async def login(
        data: LoginRequest,
        response: Response,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        user_repository_factory: Callable[
            [AsyncSession], UserByEmailRepository] = Depends(
            Provide['user_by_email_repository']),
        user_auth_service_factory: Callable[
            [UserByEmailRepository], UserAuthService] = Depends(
            Provide['user_auth_service_factory']),
        login_session_service: LoginSessionService = Depends(
            Provide['login_session_service']),
        login_session_repository_factory: Callable[
            [AsyncSession], LoginSessionRepository] = Depends(
            Provide['login_session_repository_factory']),
        session_cookie_config: SessionCookieConfig = Depends(
            Provide['session_cookie_config']),
) -> None:
    """
    Handles user login by validating the provided username and password and
    creating a session.
    
    This endpoint authenticates a user and creates a session cookie, which is
    set in the response. It uses dependencies for session management, user
    authentication, and session repository access.
    
    Args:
        data (LoginRequest): The login request data containing username and
            password.
        response (Response): The HTTP response object used to set the session
            cookie.
        session_factory (Callable[[], AsyncSession]): Factory function for
            generating database sessions.
        user_repository_factory
            (Callable[[AsyncSession], UserByEmailRepository]):
            Factory function for user repository.
        user_auth_service_factory
            (Callable[[UserByEmailRepository], UserAuthService]):
            Factory function for user authentication service.
        login_session_service (LoginSessionService): Service for login session
            management.
        login_session_repository_factory
            (Callable[[AsyncSession], LoginSessionRepository]):
            Factory function for login session repository.
        session_cookie_config (SessionCookieConfig): Configuration for session
            cookies.
    
    Returns:
        None: This function does not return a value but sets the session
            cookie in the response.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            user_repository = user_repository_factory(db_session)
            user_auth_service = user_auth_service_factory(user_repository)
            login_session_repository = login_session_repository_factory(
                db_session)
            use_case = LoginUseCase(
                user_auth_service, login_session_service,
                login_session_repository
            )
            session_cookie = await use_case(
                data.username,
                data.password,
                session_cookie_config,
            )

        response.set_cookie(
            **session_cookie.model_dump()
        )


@router.get('/verify')
@inject
async def verify(
        session: LoginSession = Depends(
            get_session,
        )
) -> LoginSession:
    """
    Verifies the validity of the current session.
    
    This endpoint checks if the user's session is valid by decoding and
    verifying the session object provided.
    
    Args:
        session (LoginSession): The session object extracted from the request.
    """
    return session


@router.post('/logout')
@inject
async def logout(
        request: Request,
        response: Response,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        login_session_repository_factory: Callable[
            [AsyncSession], LoginSessionRepository] = Depends(
            Provide['login_session_repository_factory']),
        login_session_cookie_name: str = Depends(
            Provide['login_session_cookie_name']
        )
) -> None:
    """
    Handles user logout by clearing the user's session.

    This endpoint extracts the session ID from the request's cookies, removes
    the session from the database, and deletes the session cookie.

    Args:
        request (Request): The HTTP request object used to extract the session 
            cookie.
        response (Response): The HTTP response object used to delete the 
            session cookie.
        session_factory (Callable[[], AsyncSession]): Factory function for 
            generating database sessions.
        login_session_repository_factory
            (Callable[[AsyncSession], LoginSessionRepository]):
            Factory function for login session repository.
        login_session_cookie_name (str): Name of the cookie that stores the 
            session ID.

    Returns:
        None: This function does not return a value but deletes the user's 
            session cookie.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            login_session_repository = login_session_repository_factory(
                db_session)
            use_case = LogoutUseCase(login_session_repository)
            session_id = request.cookies.get(
                login_session_cookie_name,
            )
            await use_case(session_id)

        response.delete_cookie(login_session_cookie_name)
