"""SampleItem create use case."""
from app.application.use_cases.base import AsyncBaseCreateUseCase
from app.domain.entities.sample_item import SampleItem, SampleItemCreate, \
    SampleItemUpdate


class SampleItemCreateUseCase(
    AsyncBaseCreateUseCase[
        int, SampleItem, SampleItemCreate, SampleItemUpdate]):
    """SampleItem create use case implementation."""
