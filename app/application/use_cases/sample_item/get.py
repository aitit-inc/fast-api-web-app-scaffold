"""SampleItem get use case."""

from app.application.use_cases.base import AsyncBaseGetUseCase, \
    AsyncBaseGetEntityUseCase
from app.domain.entities.sample_item import SampleItemCreate, \
    SampleItemUpdate, SampleItem, SampleItemWithMeta
from app.domain.services.sample_item_service import SampleItemService


class SampleItemGetUseCase(
    AsyncBaseGetEntityUseCase[
        int, SampleItem, SampleItemCreate, SampleItemUpdate]
):
    """SampleItem get use case."""


class SampleItemWithMetaGetUseCase(
    AsyncBaseGetUseCase[
        SampleItemWithMeta, int, SampleItem,
        SampleItemCreate, SampleItemUpdate]
):
    """SampleItemWithMeta get use case."""

    def transform(self, entity: SampleItem) -> SampleItemWithMeta:
        """Transform or process the retrieved entity."""
        lengths = SampleItemService.calculate_lengths(entity)
        merged = entity.model_dump() | {'meta_data': lengths.model_dump()}
        return SampleItemWithMeta.model_validate(merged)
