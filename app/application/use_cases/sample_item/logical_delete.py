"""SampleItem logical delete use case."""
from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemLogicalDeleteUseCase(AsyncBaseUseCase[None]):
    """SampleItem logical delete use case."""

    def __init__(self, repository: SampleItemRepository) -> None:
        """Constructor."""
        self._repository = repository

    async def __call__(self, entity_id: int) -> None:
        """Execute use case."""
        await self._repository.logical_delete(entity_id)
