"""SampleItem create use case."""
from shortuuid import uuid

from app.application.dto.sample_item import SampleItemCreate, \
    SampleItemReadDto
from app.application.use_cases.base import AsyncBaseCreateUseCase
from app.application.use_cases.sample_item.common import sample_item_to_read
from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemCreateUseCase(
    AsyncBaseCreateUseCase[
        None, SampleItem, SampleItemCreate,
        SampleItemReadDto, SampleItemRepository],
):
    """SampleItem create use case implementation."""

    def _from_create_dto(
            self,
            dto: SampleItemCreate,
            query: None,
    ) -> SampleItem:
        data_dict = dto.model_dump()
        data_dict['uuid'] = uuid()
        return SampleItem.model_validate(data_dict)

    def _to_return_dto(
            self,
            entity: SampleItem,
            query: None,
    ) -> SampleItemReadDto:
        return sample_item_to_read(entity)
