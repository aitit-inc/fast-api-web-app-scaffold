"""SampleItem create use case."""
from app.application.use_cases.base import AsyncBaseCreateUseCase
from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemCreateUseCase(
    AsyncBaseCreateUseCase[
        int, SampleItem, SampleItemRepository]):
    """SampleItem create use case implementation."""
