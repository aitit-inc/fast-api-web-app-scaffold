"""SampleItem logical delete use case."""
from app.application.use_cases.base import AsyncBaseLogicalDeleteUseCase
from app.domain.entities.sample_item import SampleItem


class SampleItemLogicalDeleteUseCase(
    AsyncBaseLogicalDeleteUseCase[int, SampleItem]
):
    """SampleItem logical delete use case."""
