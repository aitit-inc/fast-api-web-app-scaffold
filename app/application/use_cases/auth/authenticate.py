"""Authentication use case."""
from logging import getLogger
from typing import Any

from app.application.exc import InvalidCredentials
from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.factories.auth import JwtPayloadFactory
from app.domain.services.auth import Token, UserAuthService, \
    TokenType, JwtTokenService

logger = getLogger('uvicorn')


class AuthenticateUseCase(
    AsyncBaseUseCase[Token]
):
    """Authenticate use case."""

    def __init__(
            self,
            user_auth_service: UserAuthService,
            jwt_payload_factory: JwtPayloadFactory,
            jwt_token_service: JwtTokenService,
    ) -> None:
        """Initialize."""
        self._user_auth_service = user_auth_service
        self._jwt_payload_factory = jwt_payload_factory
        self._jwt_token_service = jwt_token_service

    async def __call__(
            self,
            username: str, password: str,
            *args: Any,
            with_refresh_token: bool = False,
            **kwargs: Any) -> Token:
        user = await self._user_auth_service.authenticate(
            username, password)

        if user is None:
            logger.warning('Invalid email or password.')
            raise InvalidCredentials(
                'Invalid email or password.')

        access_token = self._jwt_token_service.create_token(
            self._jwt_payload_factory(
                sub=user.uuid,
                email=str(user.email),
                is_refresh_token=False,
            ))

        if with_refresh_token:
            refresh_token = self._jwt_token_service.create_token(
                self._jwt_payload_factory(
                    sub=user.uuid,
                    email=str(user.email),
                    is_refresh_token=True,
                ))
        else:
            refresh_token = None

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=TokenType.BEARER,
        )
