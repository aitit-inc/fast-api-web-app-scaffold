"""Auth controller.

OAuth2.0 (JWT token) authentication endpoint.
--> https://fastapi.tiangolo.com/ja/tutorial/security/oauth2-jwt/
--> refresh: https://zenn.dev/tnakano/articles/072ee0fcd93433

Session cookie authentication.
--> https://medium.com/@InsightfulEnginner/session-based-authentication-with-fastapi-a-step-by-step-guide-ca19e98ce0f9
"""
from typing import Callable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.auth import JwtPayloadRead
from app.application.dto.user import UserReadDto
from app.application.use_cases.auth.authenticate import AuthenticateUseCase
from app.application.use_cases.auth.common import jwt_payload_to_read
from app.application.use_cases.auth.get_me import GetMeUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.domain.factories.auth import JwtPayloadFactory
from app.domain.repositories.user import UserByEmailRepository, \
    UserByUUIDRepository
from app.domain.services.auth import Token, UserAuthService, \
    JwtTokenService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


# pylint: disable=too-many-arguments,too-many-positional-arguments
@router.post('/token')
@inject
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        user_repository_factory: Callable[
            [AsyncSession], UserByEmailRepository] = Depends(
            Provide['user_by_email_repository']),
        user_auth_service_factory: Callable[
            [UserByEmailRepository], UserAuthService] = Depends(
            Provide['user_auth_service_factory']),
        jwt_payload_factory: JwtPayloadFactory = Depends(
            Provide['jwt_payload_factory']),
        jwt_token_service: JwtTokenService = Depends(
            Provide['jwt_token_service']),
) -> Token:
    """
    Handle user login and generate an access token.
    
    This endpoint accepts user credentials in the form of a username and
    password to authenticate the user and return a JWT token for
    authorization in further requests.
    
    Args:
        form_data (OAuth2PasswordRequestForm): An instance containing username
            and password.
        session_factory (Callable[[], AsyncSession]): A callable that provides
            an asynchronous database session.
        user_repository_factory
            (Callable[[AsyncSession], UserByEmailRepository]):
            A callable that provides a user repository to query user data.
        user_auth_service_factory (Callable[[UserByEmailRepository], 
            UserAuthService]): A callable that provides the UserAuthService to
            handle authentication.
        jwt_payload_factory (JwtPayloadFactory): A callable that provides the
            JwtPayloadFactory to generate JWT payloads.
        jwt_token_service (JwtTokenService): A callable that provides the
            JwtTokenService to generate JWT tokens.
    
    Returns:
        Token: An object containing the JWT access token upon successful
            authentication.
    
    Raises:
        HTTPException: If authentication fails due to invalid credentials or
            other issues.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            user_repository = user_repository_factory(db_session)
            user_auth_service = user_auth_service_factory(user_repository)
            use_case = AuthenticateUseCase(
                user_auth_service, jwt_payload_factory, jwt_token_service)
            token = await use_case(
                form_data.username, form_data.password,
                with_refresh_token=True
            )

            return token


@router.post('/token/refresh')
@inject
async def refresh(
        token: str = Depends(oauth2_scheme),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        user_repository_factory: Callable[
            [AsyncSession], UserByUUIDRepository] = Depends(
            Provide['user_by_uuid_repository']),
        jwt_payload_factory: JwtPayloadFactory = Depends(
            Provide['jwt_payload_factory']),
        jwt_token_service: JwtTokenService = Depends(
            Provide['jwt_token_service']),
) -> Token:
    """
    Refresh an expired JWT token.
    
    This endpoint accepts an expired or near-expiry JWT token and generates 
    a new, valid one to maintain the user's session.
    
    Args:
        token (str): The JWT token to be refreshed, typically provided in the
            Authorization header as a Bearer token.
        session_factory (Callable[[], AsyncSession]): A callable that provides
            an asynchronous database session.
        user_repository_factory
            (Callable[[AsyncSession], UserByUUIDRepository]):
            A callable that supplies a repository for retrieving user 
            information using their UUID.
        jwt_payload_factory (JwtPayloadFactory): A callable that provides the
            JwtPayloadFactory to generate JWT payloads.
        jwt_token_service (JwtTokenService): A service for managing,
            validating, and issuing JWT tokens.
    
    Returns:
        Token: A new JWT token object containing the refreshed access token 
            and optionally a refresh token if configured.
    
    Raises:
        HTTPException: If the token is invalid, expired, or if the user cannot
            be found.
    """

    async with session_factory() as db_session:
        async with db_session.begin():
            user_repository = user_repository_factory(db_session)
            use_case = RefreshTokenUseCase(
                user_repository, jwt_payload_factory, jwt_token_service)
            new_token = await use_case(token)

            return new_token


@router.get('/token/authorize')
@inject
async def authorize(
        token: str = Depends(oauth2_scheme),
        jwt_token_service: JwtTokenService = Depends(
            Provide['jwt_token_service']),
) -> JwtPayloadRead:
    """
    A sample endpoint to verify JWT token validation.
    
    This endpoint simply demonstrates how to validate a JWT token for an
    authenticated user session. It does not perform any additional logic 
    other than serving as a placeholder or validation check during 
    development.

    Args:
        token (str): A JWT token string to be validated.
        jwt_token_service (JwtTokenService): A callable that provides the
            JwtTokenService to verify JWT tokens.
    
    Returns:
        JwtPayloadRead: A read model of the JWT payload.
    """
    payload = jwt_token_service.verify_token(token)
    read_model = jwt_payload_to_read(payload)

    return read_model


@router.get('/token/me')
@inject
async def read_users_me(
        token: str = Depends(oauth2_scheme),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        user_repository_factory: Callable[
            [AsyncSession], UserByUUIDRepository] = Depends(
            Provide['user_by_uuid_repository']),
        jwt_token_service: JwtTokenService = Depends(
            Provide['jwt_token_service']),

) -> UserReadDto:
    """
    Retrieve the authenticated user's information using their JWT token.
    
    This endpoint decodes the JWT token to extract user details, retrieves 
    the user's information from the database, and returns it.

    Args:
        token (str): A JWT token string representing the authenticated user.
        session_factory (Callable[[], AsyncSession]): A callable that provides
            an asynchronous database session.
        user_repository_factory
            (Callable[[AsyncSession], UserByUUIDRepository]):
            A callable that provides a repository to query users by UUID.
        jwt_token_service (JwtTokenService): A service for managing and 
            verifying JWT tokens.
    
    Returns:
        UserReadDto: A read model of the user's information.

    Raises:
        HTTPException: If the JWT token is invalid or the user cannot be found.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            user_repository = user_repository_factory(db_session)
            use_case = GetMeUseCase(user_repository, jwt_token_service)
            user = await use_case(token)

            return user
