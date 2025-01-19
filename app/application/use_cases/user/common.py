"""Common functions for User use case."""
from typing import Sequence

from pydantic import TypeAdapter

from app.application.dto.user import UserReadDto
from app.domain.entities.user import User


def user_to_read(data: User) -> UserReadDto:
    """Convert user to user read dto."""
    return UserReadDto.model_validate(data)


def user_list_transformer(
        xs: Sequence[User]) -> Sequence[UserReadDto]:
    """Transform a list of users into user read."""
    transformed = [user_to_read(x) for x in xs]
    adapter = TypeAdapter(list[UserReadDto])
    return adapter.validate_python(transformed)
