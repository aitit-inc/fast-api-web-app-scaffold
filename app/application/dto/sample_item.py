"""SampleItem dto."""
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field

from app.domain.entities.common import MAX_LEN_SHORT
from app.domain.entities.sample_item import SampleItemBase, SampleItemLengths


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


class SampleItemReadDtoWithMeta(SampleItemReadDto):
    """SampleItem with meta."""
    meta_data: SampleItemLengths


class SampleItemGetQuery(BaseModel):
    """SampleItem entity get query."""
    with_meta: bool = PydanticField(
        Query(
            default=False,
            description='Include meta data in response',
        ))
