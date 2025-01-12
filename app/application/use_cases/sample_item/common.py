"""SampleItem base use case."""
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
