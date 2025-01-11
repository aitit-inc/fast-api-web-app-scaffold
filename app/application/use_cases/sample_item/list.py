"""SampleItem list use case."""

from app.application.use_cases.base import BaseListUseCase
from app.domain.entities.sample_item import SampleItem


class SampleItemListUseCase(
    BaseListUseCase[SampleItem],
):
    """SampleItem list use case implementation."""
