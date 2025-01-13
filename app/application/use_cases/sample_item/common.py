"""SampleItem base use case."""
from typing import Sequence

from pydantic import TypeAdapter

from app.application.dto.sample_item import SampleItemReadDto, \
    SampleItemGetQuery, SampleItemReadDtoWithMeta
from app.domain.entities.sample_item import SampleItem
from app.domain.services.sample_item_service import SampleItemService


class SampleItemUseCaseBase:
    """SampleItem base use case."""

    def _to_return_dto(
            self,
            entity: SampleItem) -> SampleItemReadDto:
        return SampleItemReadDto.model_validate(entity)


def sample_item_to_read(data: SampleItem) -> SampleItemReadDto:
    """Read SampleItem from SampleItem."""
    return SampleItemReadDto.model_validate(data)


def sample_item_with_meta_to_read(
        data: SampleItem) -> SampleItemReadDtoWithMeta:
    """Read SampleItem with meta from SampleItem."""
    lengths = SampleItemService.calculate_lengths(data)
    merged = data.model_dump() | {'meta_data': lengths.model_dump()}
    return SampleItemReadDtoWithMeta.model_validate(merged)


def sample_item_to_read_dto(
        data: SampleItem,
        query: SampleItemGetQuery,
) -> SampleItemReadDto:
    """Read SampleItem from SampleItem."""
    if query.with_meta:
        return sample_item_with_meta_to_read(data)

    return sample_item_to_read(data)


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
