"""SampleItem list use case."""
from app.application.dto.sample_item import SampleItemApiListQueryDto
from app.application.use_cases.base import BaseListUseCase
from app.domain.entities.sample_item import SampleItem


class SampleItemListUseCase(
    BaseListUseCase[SampleItemApiListQueryDto, SampleItem],
):
    """SampleItem list use case implementation."""
