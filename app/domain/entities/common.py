"""Common classes and functions for entities."""
from datetime import datetime
from typing import Any

from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlmodel import Column, Field, SQLModel


# pylint: disable=invalid-name
def DatetimeWithTimeZone(
        *args: Any,
        nullable: bool = True,
        server_default: Any = None,
        onupdate: Any = None,
        **kwargs: Any,
) -> Any:
    """Datetime with timezone."""
    kwargs['sa_column'] = Column(
        DateTime(timezone=True),
        nullable=nullable,
        server_default=server_default,
        onupdate=onupdate,
    )
    return Field(*args, **kwargs)


MAX_LEN_SHORT = 256


class BaseSQLModel(SQLModel):
    """Base SQLModel."""
    id: int | str | None

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
