"""SampleItem logical delete use case."""
from app.application.use_cases.base import AsyncBaseLogicalDeleteUseCase
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemLogicalDeleteUseCase(
    AsyncBaseLogicalDeleteUseCase[int, SampleItemRepository]
):
    """SampleItem logical delete use case."""
