"""SampleItem list use case."""
from typing import Sequence, Callable

from pydantic import TypeAdapter

from app.application.use_cases.base import AsyncBaseListEntityUseCase, \
    AsyncBaseListUseCase
from app.domain.entities.sample_item import SampleItem, SampleItemCreate, \
    SampleItemUpdate, SampleItemWithMeta
from app.domain.services.sample_item_service import SampleItemService


class SampleItemListUseCase(
    AsyncBaseListEntityUseCase[
        int, SampleItem, SampleItemCreate, SampleItemUpdate]
):
    """SampleItem list use case implementation."""


class SampleItemWithMetaListUseCase(
    AsyncBaseListUseCase[
        SampleItemWithMeta, int, SampleItem,
        SampleItemCreate, SampleItemUpdate,
    ]
):
    """SampleItemWithMeta list use case implementation."""

    @staticmethod
    def transform(
    ) -> Callable[[Sequence[SampleItem]], Sequence[SampleItemWithMeta]]:
        def transformer(
                xs: Sequence[SampleItem]) -> Sequence[SampleItemWithMeta]:
            transformed_items: list[SampleItemWithMeta] = []
            for item in xs:
                lengths = SampleItemService.calculate_lengths(item)
                merged = item.model_dump() | {
                    'meta_data': lengths.model_dump()}
                transformed_items.append(
                    SampleItemWithMeta.model_validate(merged))

            adapter = TypeAdapter(list[SampleItemWithMeta])
            return adapter.validate_python(transformed_items)

        return transformer
