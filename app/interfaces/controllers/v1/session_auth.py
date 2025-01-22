"""Session auth controller."""
from typing import Callable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.session_auth import LoginRequest, SessionCookieConfig
from app.application.use_cases.auth.login_session.login import LoginUseCase
from app.domain.repositories.login_session import LoginSessionRepository
from app.domain.repositories.user import UserByEmailRepository
from app.domain.services.auth.base import UserAuthService
from app.domain.services.auth.login_session import LoginSessionService
from app.interfaces.controllers.v1.path import AUTH_SESSION_PREFIX

router = APIRouter(
    prefix=AUTH_SESSION_PREFIX,
    tags=['auth-session'],
)


# pylint: disable=too-many-arguments,too-many-positional-arguments
@router.post('/login')
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
