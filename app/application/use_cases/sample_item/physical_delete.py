"""SampleItem physical delete use case."""
from app.application.use_cases.base import AsyncBasePhysicalDeleteUseCase
from app.domain.entities.sample_item import SampleItem


class SampleItemPhysicalDeleteUseCase(
    AsyncBasePhysicalDeleteUseCase[int, SampleItem]
):
    """SampleItem physical delete use case."""
