"""Token auth controller."""
from typing import Callable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.token_auth import JwtPayloadRead
from app.application.dto.user import UserReadDto
from app.application.use_cases.auth.token.authenticate import \
    AuthenticateUseCase
from app.application.use_cases.auth.token.common import jwt_payload_to_read
from app.application.use_cases.auth.token.get_me import GetMeUseCase
from app.application.use_cases.auth.token.refresh import RefreshTokenUseCase
from app.application.use_cases.user.get_by_uuid import UserGetByUUIDUseCase
from app.domain.factories.token_auth import JwtPayloadFactory
from app.domain.repositories.user import UserByEmailRepository, \
    UserByUUIDRepository
from app.domain.services.auth.base import UserAuthService
from app.domain.services.auth.token import Token, JwtTokenService, JwtPayload
from app.interfaces.controllers.v1.path import AUTH_TOKEN_PREFIX, \
    TOKEN_ENDPOINT, \
    REFRESH_ENDPOINT, EXPLICIT_TOKEN_ME_ENDPOINT
from app.interfaces.middlewares.auth_middleware import \
    get_token_payload, oauth2_scheme

router = APIRouter(
    prefix=AUTH_TOKEN_PREFIX,
    tags=['auth-token'],
)


# pylint: disable=too-many-arguments,too-many-positional-arguments
@router.post(TOKEN_ENDPOINT)
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


@router.post(REFRESH_ENDPOINT)
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


@router.get('/verify')
@inject
async def verify(
        payload: JwtPayload = Depends(
            get_token_payload
        ),
) -> JwtPayloadRead:
    """
    A sample endpoint to verify JWT token validation.
    
    This endpoint demonstrates how to retrieve the validated JWT payload that 
    the authentication middleware has already processed. It primarily serves 
    as an example for extracting and returning the payload during development.
    
    Args:
        payload (JwtPayload): The JWT payload extracted from the request.
    
    Returns:
        JwtPayloadRead: A read model of the JWT payload.
    """
    read_model = jwt_payload_to_read(payload)

    return read_model


@router.get('/me')
@inject
async def read_users_me(
        payload: JwtPayload = Depends(
            get_token_payload
        ),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        user_repository_factory: Callable[
            [AsyncSession], UserByUUIDRepository] = Depends(
            Provide['user_by_uuid_repository']),
) -> UserReadDto:
    """
    Retrieve the authenticated user's information using their JWT token.
    
    This endpoint demonstrates how to use the authentication middleware to
    retrieve the already verified JWT payload, which includes essential user
    information such as the user ID. Using the user ID extracted from the 
    payload, this endpoint queries the database to fetch and return the 
    user's data in a structured format.
    
    Args:
        payload (JwtPayload): The JWT payload extracted from the request and
            verified by the authentication middleware.
        session_factory (Callable[[], AsyncSession]): A callable that provides
            an asynchronous database session.
        user_repository_factory 
            (Callable[[AsyncSession], UserByUUIDRepository]):
            A callable that supplies a repository for retrieving user
            information using their UUID.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            user_repository = user_repository_factory(db_session)
            use_case = UserGetByUUIDUseCase(user_repository)
            read_data = await use_case(payload.sub, None, None)

            return read_data


@router.get(EXPLICIT_TOKEN_ME_ENDPOINT)
@inject
async def explicit_auth_and_read_users_me(
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
    
    This endpoint explicitly implements token verification within the 
    endpoint, serving as an example of how to validate a JWT token and 
    authenticate a user to retrieve their information from the database.
    
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
