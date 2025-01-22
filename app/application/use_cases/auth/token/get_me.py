"""Get me use case."""
from logging import getLogger
from typing import Any

from app.application.dto.user import UserReadDto
from app.application.exc import EntityNotFound
from app.application.use_cases.base import AsyncBaseUseCase
from app.application.use_cases.user.common import user_to_read
from app.domain.repositories.user import UserByUUIDRepository
from app.domain.services.auth.token import JwtTokenService

logger = getLogger('uvicorn')


class GetMeUseCase(
    AsyncBaseUseCase[UserReadDto]
):
    """Get me use case."""

    def __init__(
            self,
            user_repository: UserByUUIDRepository,
            jwt_token_service: JwtTokenService,
    ) -> None:
        """Initialize."""
        self._user_repository = user_repository
        self._jwt_token_service = jwt_token_service

    async def __call__(self, token: str,
                       *args: Any, **kwargs: Any) -> UserReadDto:
        payload = self._jwt_token_service.verify_token(token)
        user = await self._user_repository.get_by_id(payload.sub)
        if user is None:
            logger.error('User not found by UUID: %s', payload.sub)
            raise EntityNotFound(
                f'User not found by UUID: {payload.sub}')

        return user_to_read(user)
