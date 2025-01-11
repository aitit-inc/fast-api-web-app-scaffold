"""SampleItem get use case."""

from app.application.use_cases.base import AsyncBaseGetUseCase
from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemGetUseCase(
    AsyncBaseGetUseCase[
        int, SampleItem, SampleItemRepository]
):
    """SampleItem get use case."""
