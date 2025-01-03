"""SampleItem list use case."""

from app.application.use_cases.base import AsyncBaseListUseCase
from app.domain.entities.sample_item import SampleItem, SampleItemCreate, \
    SampleItemUpdate, SampleItemReadWithMeta, SampleItemRead


class SampleItemListUseCase(
    AsyncBaseListUseCase[
        SampleItemRead, int, SampleItem, SampleItemCreate, SampleItemUpdate]
):
    """SampleItem list use case implementation."""


class SampleItemWithMetaListUseCase(
    AsyncBaseListUseCase[
        SampleItemReadWithMeta, int, SampleItem,
        SampleItemCreate, SampleItemUpdate,
    ]
):
    """SampleItemWithMeta list use case implementation."""
