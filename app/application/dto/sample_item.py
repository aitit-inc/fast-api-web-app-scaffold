"""SampleItem dto."""
from datetime import datetime

from sqlmodel import SQLModel, Field

from app.domain.entities.common import MAX_LEN_SHORT
from app.domain.entities.sample_item import SampleItemBase


class SampleItemCreate(SampleItemBase):
    """SampleItem entity create."""


class SampleItemUpdateDto(SQLModel):
    """SampleItem entity update."""
    name: str | None = Field(max_length=MAX_LEN_SHORT, default=None)
    description: str | None = None


class SampleItemReadDto(SampleItemBase):
    """SampleItem entity read."""
    uuid: str
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
