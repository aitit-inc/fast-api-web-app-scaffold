"""User list use case."""
from app.application.dto.user import UserApiListQueryDto
from app.application.use_cases.base import BaseListUseCase
from app.domain.entities.user import User


class UserListUseCase(
    BaseListUseCase[UserApiListQueryDto, User],
):
    """User list use case implementation."""
