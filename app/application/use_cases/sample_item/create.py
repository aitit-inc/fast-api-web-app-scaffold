"""SampleItem create use case."""
from shortuuid import uuid

from app.application.dto.sample_item import SampleItemCreate, \
    SampleItemReadDto
from app.application.use_cases.base import AsyncBaseCreateUseCase
from app.application.use_cases.sample_item.common import sample_item_to_read
from app.domain.entities.sample_item import SampleItem


class SampleItemCreateUseCase(
    AsyncBaseCreateUseCase[
        int, None, SampleItem, SampleItemCreate,
        SampleItemReadDto],
):
    """SampleItem create use case implementation."""

    def _from_create_dto(
            self,
            dto: SampleItemCreate,
            query: None,
    ) -> SampleItem:
        data_dict = dto.model_dump()
        data_dict['uuid'] = self._gen_uuid()
        return SampleItem.model_validate(data_dict)

    def _to_return_dto(
            self,
            entity: SampleItem,
            query: None,
    ) -> SampleItemReadDto:
        return sample_item_to_read(entity)

    @staticmethod
    def _gen_uuid() -> str:
        return uuid()
