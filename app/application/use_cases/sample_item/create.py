"""SampleItem create use case."""
from shortuuid import uuid

from app.application.dto.sample_item import SampleItemCreate, SampleItemReadDto
from app.application.use_cases.base import AsyncBaseCreateUseCase
from app.application.use_cases.sample_item.base import SampleItemUseCaseBase
from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemCreateUseCase(
    SampleItemUseCaseBase,
    AsyncBaseCreateUseCase[
       SampleItem, SampleItemCreate, SampleItemReadDto, SampleItemRepository],
):
    """SampleItem create use case implementation."""

    def _from_create_dto(self, dto: SampleItemCreate) -> SampleItem:
        data_dict = dto.model_dump()
        data_dict['uuid'] = uuid()
        return SampleItem.model_validate(data_dict)
