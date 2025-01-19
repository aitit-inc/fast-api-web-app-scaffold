"""Token refresh use case."""
from logging import getLogger
from typing import Any

from app.application.exc import Unauthorized
from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.factories.auth import JwtPayloadFactory
from app.domain.repositories.user import UserByUUIDRepository
from app.domain.services.auth import Token, JwtTokenService, \
    TokenType

logger = getLogger('uvicorn')


class RefreshTokenUseCase(
    AsyncBaseUseCase[Token]
):
    """Token refresh use case."""

    def __init__(
            self,
            user_repository: UserByUUIDRepository,
            jwt_payload_factory: JwtPayloadFactory,
            jwt_token_service: JwtTokenService,
    ) -> None:
        """Initialize."""
        self._user_repository = user_repository
        self._jwt_payload_factory = jwt_payload_factory
        self._jwt_token_service = jwt_token_service

    async def __call__(
            self,
            refresh_token: str,
            *args: Any, **kwargs: Any,
    ) -> Token:
        payload = self._jwt_token_service.verify_token(refresh_token)
        if payload.is_refresh_token is False:
            logger.error('Invalid refresh token. is_refresh_token: %s',
                         payload.is_refresh_token)
            raise Unauthorized('Invalid refresh token.')

        user = await self._user_repository.get_by_id(payload.sub)
        if user is None:
            logger.error('User not found by UUID: %s', payload.sub)
            raise Unauthorized('Invalid refresh token.')

        access_token = self._jwt_token_service.create_token(
            self._jwt_payload_factory(
                sub=user.uuid,
                email=str(user.email),
                is_refresh_token=False,
            ))

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,  # Don't update refresh_token
            token_type=TokenType.BEARER,
        )
