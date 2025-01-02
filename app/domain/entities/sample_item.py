"""SampleItem entity."""
from datetime import datetime

from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel

from app.domain.entities.common import DatetimeWithTimeZone

MAX_LEN = 256


class SampleItemBase(SQLModel):
    """SampleItem entity base class."""
    name: str = Field(
        max_length=MAX_LEN, nullable=False,
        description='SampleItem name, description for pydantic and openapi',
        sa_column_kwargs={'comment': 'SampleItem name, comment for db'}
    )
    description: str | None = Field(
        nullable=True,
        description='SampleItem description for pydantic and openapi',
        sa_column_kwargs={'comment': 'SampleItem description for db'}
    )


class SampleItem(SampleItemBase, table=True):
    """SampleItem entity."""
    __tablename__ = "sample_items"
    id: int | None = Field(default=None, primary_key=True)

    is_deleted: bool | None = Field(default=False, nullable=False)
    created_at: datetime | None = DatetimeWithTimeZone(
        server_default=func.now(),
        nullable=False,
        default=None)
    updated_at: datetime | None = DatetimeWithTimeZone(
        server_default=func.now(),
        nullable=False,
        default=None,
        onupdate=func.now())
    deleted_at: datetime | None = DatetimeWithTimeZone(
        nullable=True,
        default=None, )


class SampleItemCreate(SampleItemBase):
    """SampleItem entity create."""


class SampleItemRead(SampleItemBase):
    """SampleItem entity read."""
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class SampleItemUpdate(SQLModel):
    """SampleItem entity update."""
    name: str | None = Field(max_length=MAX_LEN, default=None)
    description: str | None = None
