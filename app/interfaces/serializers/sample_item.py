"""Serializer for SampleItem API data from/to domain data."""
from datetime import datetime
from typing import Sequence

from fastapi import Query
from pydantic import TypeAdapter, Field

from app.application.dto.sample_item import SampleItemReadDto
from app.domain.entities.sample_item import SampleItemLengths, SampleItem
from app.domain.services.sample_item_service import SampleItemService
from app.domain.value_objects.api_query import ApiListQuery
from app.interfaces.serializers.base import ApiListQueryDtoBaseModel


class SampleItemReadDtoWithMeta(SampleItemReadDto):
    """SampleItem with meta."""
    meta_data: SampleItemLengths


# TODO: Delete
def sample_item_to_read(data: SampleItem) -> SampleItemReadDto:
    """Read SampleItem from SampleItem."""
    return SampleItemReadDto.model_validate(data)


def sample_item_with_meta_to_read(
        data: SampleItem) -> SampleItemReadDtoWithMeta:
    """Read SampleItem with meta from SampleItem."""
    lengths = SampleItemService.calculate_lengths(data)
    merged = data.model_dump() | {'meta_data': lengths.model_dump()}
    return SampleItemReadDtoWithMeta.model_validate(merged)


def sample_item_list_transformer(
        xs: Sequence[SampleItem]) -> Sequence[SampleItemReadDto]:
    """Transform a list of SampleItems into SampleItemRead."""
    transformed = [sample_item_to_read(x) for x in xs]
    adapter = TypeAdapter(list[SampleItemReadDto])
    return adapter.validate_python(transformed)


def sample_item_with_meta_list_transformer(
        xs: Sequence[SampleItem]) -> Sequence[SampleItemReadDtoWithMeta]:
    """Transform a list of SampleItems into SampleItemReadWithMeta."""
    transformed = [sample_item_with_meta_to_read(x) for x in xs]
    adapter = TypeAdapter(list[SampleItemReadDtoWithMeta])
    return adapter.validate_python(transformed)


# ###########################################################
# Filter and Sort
class SampleItemApiListQueryDto(ApiListQueryDtoBaseModel):
    """SampleItem filter."""
    __entity_cls__ = SampleItem
    name__eq: str | None = None
    name__like: str | None = Field(Query(
        default=None,
        description='Fuzzy search query for SampleItem name, following '
                    'PostgreSQL ILIKE semantics',
        example='%foo%',
    ))
    created_at__gte: datetime | None = None
    created_at__lte: datetime | None = None
    created_at__asc: bool | None = None
    created_at__desc: bool | None = None

    def to_domain(self) -> ApiListQuery:
        """Convert to domain object."""
        return ApiListQuery(
            queries=self.model_dump(exclude_none=True),
        )
