"""SampleItem create use case."""
from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.entities.sample_item import SampleItem, SampleItemCreate
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemCreateUseCase(AsyncBaseUseCase[SampleItem]):
    """SampleItem create use case."""

    def __init__(self, repository: SampleItemRepository) -> None:
        """Constructor."""
        self._repository = repository

    async def __call__(self, data: SampleItemCreate) -> SampleItem:
        """Execute use case."""
        return await self._repository.add(data)
