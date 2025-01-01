"""Common classes and functions for entities."""
from typing import Any

from sqlmodel import Column, DateTime, Field


def DatetimeWithTimeZone(
        nullable: bool=True,
        server_default: Any = None,
        onupdate: Any = None,
        *args: Any,
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
