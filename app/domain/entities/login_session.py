"""Login session entity."""
from datetime import datetime

from sqlalchemy.sql import func
from sqlmodel import SQLModel, Field

from app.domain.entities.common import DatetimeWithTimeZone


class LoginSession(SQLModel, table=True):
    """Login session entity."""
    __tablename__ = "login_sessions"
    id: str = Field(max_length=128, primary_key=True, index=True)
    user_id: int = Field(nullable=False)
    user_uuid: str = Field(nullable=False)
    expires_at: datetime = DatetimeWithTimeZone(nullable=False)

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
