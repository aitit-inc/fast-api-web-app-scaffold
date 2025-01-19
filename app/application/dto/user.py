"""User dto."""
from datetime import datetime

from fastapi import Query
from pydantic import Field as PydanticField
from sqlmodel import SQLModel, Field

from app.application.dto.base import ApiListQueryDtoBaseModel
from app.domain.entities.common import MAX_LEN_SHORT
from app.domain.entities.user import UserBase, User


class UserCreate(UserBase):
    """User entity create."""
    password: str = Field(max_length=128, nullable=False)


class UserReadDto(UserBase):
    """User entity read."""
    uuid: str
    is_active: bool
    is_superuser: bool
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class UserUpdate(SQLModel):
    """User entity update."""
    last_login: datetime | None = None
    first_name: str | None = Field(max_length=MAX_LEN_SHORT, default=None)
    last_name: str | None = Field(max_length=MAX_LEN_SHORT, default=None)


class UserApiListQueryDto(ApiListQueryDtoBaseModel):
    """User filter."""
    __entity_cls__ = User
    first_name__eq: str | None = None
    first_name__like: str | None = PydanticField(Query(
        default=None,
        description='Fuzzy search query for User first name, following '
                    'PostgreSQL ILIKE semantics, e.g. "%foo%" or "f_o"',
    ))
    last_name__eq: str | None = None
    last_name__like: str | None = PydanticField(Query(
        default=None,
        description='Fuzzy search query for User first name, following '
                    'PostgreSQL ILIKE semantics, e.g. "%foo%" or "f_o"',
    ))
    email__eq: str | None = None
    email__like: str | None = PydanticField(Query(
        default=None,
        description='Fuzzy search query for User email, following '
                    'PostgreSQL ILIKE semantics, e.g. "%foo%" or "f_o"',
    ))
