"""SampleItem get by uuid use case."""
from app.application.dto.sample_item import SampleItemReadDto, \
    SampleItemReadDtoWithMeta, SampleItemGetQuery
from app.application.use_cases.base import AsyncBaseGetByIdUseCase
from app.application.use_cases.sample_item.common import \
    sample_item_to_read_dto
from app.domain.entities.sample_item import SampleItem

ReturnType = SampleItemReadDto | SampleItemReadDtoWithMeta


class SampleItemGetByUUIDUseCase(
    AsyncBaseGetByIdUseCase[
        str, SampleItemGetQuery, None, SampleItem,
        ReturnType]
):
    """SampleItem get use case."""

    def _to_return_dto(self, entity: SampleItem, query: SampleItemGetQuery,
                       body: None) -> ReturnType:
        return sample_item_to_read_dto(entity, query)
