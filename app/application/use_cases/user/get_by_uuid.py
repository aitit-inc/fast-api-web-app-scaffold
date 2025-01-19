"""User get use case."""
from app.application.dto.user import UserReadDto
from app.application.use_cases.base import AsyncBaseGetByIdUseCase
from app.application.use_cases.user.common import user_to_read
from app.domain.entities.user import User


class UserGetByUUIDUseCase(
    AsyncBaseGetByIdUseCase[
        str, None, None, User, UserReadDto]
):
    """User get use case."""

    def _to_return_dto(self, entity: User, query: None, body: None
                       ) -> UserReadDto:
        return user_to_read(entity)
