"""Common classes and functions for entities."""
from typing import Any

from sqlalchemy.types import DateTime
from sqlmodel import Column, Field


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


LEN_64 = 64
LEN_128 = 128
LEN_256 = 256
LEN_512 = 512
LEN_1024 = 1024
