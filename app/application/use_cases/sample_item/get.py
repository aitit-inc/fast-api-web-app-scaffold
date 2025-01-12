"""SampleItem get use case."""
from app.application.dto.sample_item import SampleItemReadDto, \
    SampleItemGetQuery, SampleItemReadDtoWithMeta
from app.application.use_cases.base import AsyncBaseGetByIdUseCase
from app.application.use_cases.sample_item.common import \
    sample_item_to_read_dto
from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.sample_item import SampleItemRepository

ReturnType = SampleItemReadDto | SampleItemReadDtoWithMeta


class SampleItemGetByIdUseCase(
    AsyncBaseGetByIdUseCase[
        int, SampleItemGetQuery, None, SampleItem,
        ReturnType, SampleItemRepository]
):
    """SampleItem get use case."""

    def _to_return_dto(self, entity: SampleItem, query: SampleItemGetQuery,
                       body: None) -> ReturnType:
        return sample_item_to_read_dto(entity, query)
