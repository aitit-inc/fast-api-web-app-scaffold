"""SampleItem get use case."""

from app.application.exc import EntityNotFound
from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.entities.sample_item import SampleItemRead
from app.domain.repositories.sample_item import SampleItemRepository
from app.domain.services.sample_item_service import SampleItemService
from app.domain.value_objects.sample_item_lengths import SampleItemLengths


class SampleItemWithMeta(SampleItemRead):
    """SampleItem with meta."""
    meta_data: SampleItemLengths


class SampleItemGetUseCase(AsyncBaseUseCase[SampleItemWithMeta]):
    """SampleItem get use case."""

    def __init__(self, repository: SampleItemRepository) -> None:
        """Constructor."""
        self._repository = repository

    async def __call__(self, item_id: int) -> SampleItemWithMeta:
        """Execute use case."""
        item = await self._repository.get_by_id(item_id)
        if not item:
            raise EntityNotFound(
                EntityNotFound.to_msg(item_id),
                detail=f'Entity with ID {item_id} does not exist.'
            )

        lengths = SampleItemService.calculate_lengths(item)
        merged = item.model_dump() | {'meta_data': lengths.model_dump()}
        return SampleItemWithMeta.model_validate(merged)
