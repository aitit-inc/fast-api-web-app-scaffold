"""SampleItem get use case."""

from app.application.use_cases.base import AsyncBaseGetUseCase
from app.domain.entities.sample_item import SampleItemCreate, \
    SampleItemUpdate, SampleItem, SampleItemReadWithMeta, SampleItemRead


class SampleItemGetUseCase(
    AsyncBaseGetUseCase[
        SampleItemRead, int, SampleItem, SampleItemCreate, SampleItemUpdate]
):
    """SampleItem get use case."""


class SampleItemWithMetaGetUseCase(
    AsyncBaseGetUseCase[
        SampleItemReadWithMeta, int, SampleItem,
        SampleItemCreate, SampleItemUpdate]
):
    """SampleItemWithMeta get use case."""
