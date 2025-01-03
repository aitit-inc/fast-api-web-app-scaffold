"""SampleItem entity."""
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel

from app.domain.entities.common import DatetimeWithTimeZone, MAX_LEN_SHORT


class SampleItemBase(SQLModel):
    """SampleItem entity base class."""
    name: str = Field(
        max_length=MAX_LEN_SHORT, nullable=False,
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
    id: int | None = Field(default=None, primary_key=True, index=True)

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


class SampleItemCreate(SampleItemBase):
    """SampleItem entity create."""


class SampleItemRead(SampleItemBase):
    """SampleItem entity read."""
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class SampleItemUpdate(SQLModel):
    """SampleItem entity update."""
    name: str | None = Field(max_length=MAX_LEN_SHORT, default=None)
    description: str | None = None


class SampleItemLengths(BaseModel):
    """Value object to represent lengths of SampleItem fields."""
    name_length: int
    description_length: int


class SampleItemWithMeta(SampleItemRead):
    """SampleItem with meta."""
    meta_data: SampleItemLengths
