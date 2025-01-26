"""SampleItem dto."""
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field

from app.domain.entities.common import LEN_256
from app.domain.entities.sample_item import SampleItemBase, \
    SampleItemLengths, SampleItem
from app.application.dto.base import ApiListQueryDtoBaseModel


class SampleItemCreate(SampleItemBase):
    """SampleItem entity create."""


class SampleItemUpdateDto(SQLModel):
    """SampleItem entity update."""
    name: str | None = Field(max_length=LEN_256, default=None)
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


class SampleItemApiListQueryDto(ApiListQueryDtoBaseModel):
    """SampleItem filter."""
    __entity_cls__ = SampleItem
    name__eq: str | None = None
    name__like: str | None = PydanticField(Query(
        default=None,
        description='Fuzzy search query for SampleItem name, following '
                    'PostgreSQL ILIKE semantics, e.g. "%foo%" or "f_o"',
    ))
    created_at__gte: datetime | None = None
    created_at__lte: datetime | None = None
    created_at__asc: bool | None = None
    created_at__desc: bool | None = None
