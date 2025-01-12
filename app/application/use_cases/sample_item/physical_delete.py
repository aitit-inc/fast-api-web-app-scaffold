"""SampleItem physical delete use case."""
from app.application.use_cases.base import AsyncBasePhysicalDeleteUseCase
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemPhysicalDeleteUseCase(
    AsyncBasePhysicalDeleteUseCase[int, SampleItemRepository]
):
    """SampleItem physical delete use case."""
