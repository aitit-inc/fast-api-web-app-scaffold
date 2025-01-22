"""User auth service implementation.

ref: https://fastapi.tiangolo.com/ja/tutorial/security/oauth2-jwt/
"""
from datetime import datetime
from logging import getLogger
from typing import Callable

from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from app.application.exc import Unauthorized
from app.domain.entities.user import User
from app.domain.repositories.user import UserByEmailRepository
from app.domain.services.auth.token import JwtTokenService, JwtPayload
from app.domain.services.auth.base import UserAuthService

logger = getLogger('uvicorn')


class InDBUserTokenAuthService(UserAuthService):
    """In DB user auth service."""

    @staticmethod
    def create_factory(
            get_now: Callable[[], datetime],
    ) -> 'Callable[[UserByEmailRepository], UserAuthService]':
        """Create factory."""
        return lambda user_repository: InDBUserTokenAuthService(
            user_repository, get_now
        )

    def __init__(
            self,
            user_repository: UserByEmailRepository,
            get_now: Callable[[], datetime],
    ) -> None:
        """Initialize."""
        self._get_now = get_now
        self._user_repository = user_repository
        self._pwd_context = CryptContext(
            schemes=['bcrypt'], deprecated='auto')

    async def authenticate(self, username: str, password: str) -> User | None:
        """Authenticate user."""
        user = await self._user_repository.get_by_id(username)
        if user is None:
            return None

        if not self._verify_password(password, user.password_hash):
            return None

        await self._user_repository.update(
            str(user.email),
            {'last_login': self._get_now()}
        )

        return user

    def hash_password(self, password: str) -> str:
        """Hash password."""
        return self._pwd_context.hash(password)

    def _verify_password(
            self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(
            plain_password, hashed_password)


class JwtTokenServiceImpl(JwtTokenService):
    """JWT token service implementation."""

    def __init__(
            self,
            token_secret_key: str,
            token_algorithm: str,
            audience: str,
            issuer: str,
    ) -> None:
        """Initialize."""
        self._pwd_context = CryptContext(
            schemes=['bcrypt'], deprecated='auto')
        self._token_secret_key = token_secret_key
        self._token_algorithm = token_algorithm
        self._audience = audience
        self._issuer = issuer

    def create_token(self, data: JwtPayload) -> str:
        """Create access token."""
        encoded_jwt: str = jwt.encode(
            data.model_dump(exclude_none=True),
            self._token_secret_key,
            algorithm=self._token_algorithm)

        return encoded_jwt

    def verify_token(self, token: str) -> JwtPayload:
        """Verify token.

        Args:
            token (str): JWT token.

        Returns:
            JwtPayload: JWT payload.

        Exceptions:
            Unauthorized: Invalid token.
        """
        try:
            payload_dict = jwt.decode(
                token,
                self._token_secret_key,
                algorithms=[self._token_algorithm],
                audience=self._audience,
                issuer=self._issuer,
            )

            payload = JwtPayload.model_validate(payload_dict)
            return payload

        except JWTError as err:
            logger.warning('Could not validate credentials: %s', err)
            raise Unauthorized(
                'Could not validate credentials'
            ) from err
