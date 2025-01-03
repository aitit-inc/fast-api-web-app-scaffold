"""User entity."""
import uuid as uuid_pkg
from datetime import datetime

from pydantic import EmailStr
from sqlalchemy.sql import func
from sqlmodel import SQLModel, Field, AutoString

from app.domain.entities.common import MAX_LEN_SHORT, DatetimeWithTimeZone


class UserBase(SQLModel):
    """User entity base."""
    first_name: str | None = Field(max_length=MAX_LEN_SHORT, default=None)
    last_name: str | None = Field(max_length=MAX_LEN_SHORT, default=None)
    email: EmailStr = Field(
        unique=True, index=True, nullable=False, sa_type=AutoString)


class User(UserBase, table=True):
    """User entity."""
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True, index=True)
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        unique=True, index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    last_login: datetime | None = DatetimeWithTimeZone(
        default=None,
    )

    created_at: datetime | None = DatetimeWithTimeZone(
        server_default=func.now(),  # pylint: disable=not-callable
        nullable=False,
        default=None)
    updated_at: datetime | None = DatetimeWithTimeZone(
        server_default=func.now(),  # pylint: disable=not-callable
        nullable=False,
        default=None,
        onupdate=func.now(),  # pylint: disable=not-callable
    )
    deleted_at: datetime | None = DatetimeWithTimeZone(default=None)


class UserCreate(UserBase):
    """User entity create."""
    password: str = Field(max_length=128, nullable=False)


class UserRead(UserBase):
    """User entity read."""
    uuid: uuid_pkg.UUID
    is_active: bool
    is_superuser: bool
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class UserUpdate(SQLModel):
    """User entity update."""
    first_name: str | None = Field(max_length=MAX_LEN_SHORT, default=None)
    last_name: str | None = Field(max_length=MAX_LEN_SHORT, default=None)
