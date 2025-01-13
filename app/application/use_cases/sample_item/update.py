"""SampleItem update use case."""
from typing import Any

from app.application.dto.sample_item import SampleItemUpdateDto, \
    SampleItemReadDto
from app.application.use_cases.base import AsyncBaseUpdateUseCase, ReturnT
from app.application.use_cases.sample_item.common import sample_item_to_read
from app.domain.entities.sample_item import SampleItem


class SampleItemUpdateUseCase(
    AsyncBaseUpdateUseCase[
        int, None, SampleItem, SampleItemUpdateDto, SampleItemReadDto]
):
    """SampleItem update use case."""

    def _to_return_dto(
            self,
            entity: SampleItem,
            query: None) -> ReturnT:
        return sample_item_to_read(entity)

    def _from_update_dto(
            self,
            dto: SampleItemUpdateDto,
            query: None) -> dict[str, Any]:
        return dto.model_dump(exclude_unset=True)
