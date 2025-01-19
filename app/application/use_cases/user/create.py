"""User create use case."""
from shortuuid import uuid

from app.application.dto.user import UserCreate, UserReadDto
from app.application.use_cases.base import AsyncBaseCreateUseCase
from app.application.use_cases.user.common import user_to_read
from app.domain.entities.user import User
from app.domain.repositories.user import UserByUUIDRepository
from app.domain.services.auth import UserAuthService


class UserCreateUseCase(
    AsyncBaseCreateUseCase[
        str, None, User, UserCreate,
        UserReadDto],
):
    """User create use case implementation."""

    def __init__(
            self,
            repository: UserByUUIDRepository,
            user_auth_service: UserAuthService,
    ):
        super().__init__(repository)
        self._user_auth_service = user_auth_service

    def _from_create_dto(
            self,
            dto: UserCreate,
            query: None,
    ) -> User:
        data_dict = dto.model_dump()
        data_dict['uuid'] = uuid()
        data_dict['password_hash'] = self._user_auth_service.hash_password(
            data_dict['password']
        )
        del data_dict['password']

        return User.model_validate(data_dict)

    def _to_return_dto(
            self,
            entity: User,
            query: None,
    ) -> UserReadDto:
        return user_to_read(entity)
