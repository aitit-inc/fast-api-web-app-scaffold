"""SampleItem update use case."""
from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.entities.sample_item import SampleItem, SampleItemUpdate
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemUpdateUseCase(AsyncBaseUseCase[SampleItem]):
    """SampleItem update use case."""

    def __init__(self, repository: SampleItemRepository) -> None:
        """Constructor."""
        self._repository = repository

    async def __call__(self, entity_id: int,
                       data: SampleItemUpdate) -> SampleItem:
        """Execute use case."""
        return await self._repository.update(entity_id, data)
