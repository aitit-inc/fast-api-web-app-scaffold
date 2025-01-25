"""Access token authorizer."""
from abc import ABC, abstractmethod
from enum import Enum
from logging import getLogger
from typing import Callable

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exc import Unauthorized
from app.domain.repositories.login_session import LoginSessionRepository
from app.domain.services.auth.login_session import LoginSessionService
from app.domain.services.auth.token import JwtTokenService

logger = getLogger('uvicorn')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class AuthMethod(str, Enum):
    """Auth method."""
    BEARER_ACCESS_TOKEN = 'bearer_access_token'
    SESSION_COOKIE = 'session_cookie'


class AuthorizerBase(ABC):
    """Authorizer."""

    @abstractmethod
    async def authorize(self, request: Request) -> Request:
        """Authorize."""


class AccessTokenAuthorizer(AuthorizerBase):
    """Access token authorizer."""

    def __init__(
            self,
            jwt_token_service: JwtTokenService,
    ):
        self._jwt_token_service = jwt_token_service

    async def authorize(self, request: Request) -> Request:
        """Authorize."""
        # Extract token from Authorization header
        try:
            token = await oauth2_scheme(request)
        except HTTPException as _err:
            logger.warning('HTTPException: %s', _err)
            token = None

        if token is None:
            logger.warning(
                'Failed to extract token from Authorization header.')
            raise Unauthorized('Invalid or missing token.')

        payload = self._jwt_token_service.verify_token(token)

        request.state.user_id = payload.sub
        request.state.payload = payload

        return request


class SessionCookieAuthorizer(AuthorizerBase):
    """Session cookie authorizer."""

    @staticmethod
    def create_factory(
            login_session_repository_factory: Callable[
                [AsyncSession], LoginSessionRepository],
            login_session_service: LoginSessionService,
            login_session_cookie_name: str,
    ) -> Callable[[Callable[[], AsyncSession]], 'SessionCookieAuthorizer']:
        """Create factory."""
        return lambda session_factory: SessionCookieAuthorizer(
            session_factory,
            login_session_repository_factory,
            login_session_service,
            login_session_cookie_name,
        )

    def __init__(
            self,
            session_factory: Callable[[], AsyncSession],
            login_session_repository_factory: Callable[
                [AsyncSession], LoginSessionRepository],
            login_session_service: LoginSessionService,
            login_session_cookie_name: str,
    ):
        self._login_session_repository_factory = \
            login_session_repository_factory
        self._session_factory = session_factory
        self._login_session_service = login_session_service
        self._login_session_cookie_name = login_session_cookie_name

    async def authorize(self, request: Request) -> Request:
        """Authorize."""
        session_id = request.cookies.get(
            self._login_session_cookie_name,
        )
        if session_id is None:
            logger.warning('Failed to extract session_id from cookies.')
            raise Unauthorized('Invalid or missing session.')

        async with self._session_factory() as db_session:
            async with db_session.begin():
                login_session_repository = \
                    self._login_session_repository_factory(db_session)

                session = await login_session_repository.get_by_id(
                    session_id)
                if session is None:
                    logger.warning(
                        'Failed to get session from DB by session_id.')
                    raise Unauthorized('Invalid or missing session.')

            request.state.user_id = session.user_id
            request.state.session = session

            return request
