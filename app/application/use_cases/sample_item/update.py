"""SampleItem update use case."""
from app.application.dto.sample_item import SampleItemUpdateDto, \
    SampleItemReadDto
from app.application.use_cases.base import AsyncBaseUseCase
from app.application.use_cases.sample_item.base import SampleItemUseCaseBase
from app.domain.repositories.base import UpdateT
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemUpdateUseCase(
    SampleItemUseCaseBase,
    AsyncBaseUseCase[SampleItemReadDto]):
    """SampleItem update use case."""

    def __init__(self, repository: SampleItemRepository) -> None:
        """Constructor."""
        self._repository = repository

    async def __call__(self, entity_id: int,
                       dto: SampleItemUpdateDto) -> SampleItemReadDto:
        """Execute use case."""
        data = self._from_update_dto(dto)
        entity = await self._repository.update(entity_id, data)

        return self._to_return_dto(entity)

    def _from_update_dto(self, data: SampleItemUpdateDto) -> UpdateT:
        return data.model_dump(exclude_unset=True)
