"""SampleItem repository interface."""
from abc import ABC

from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.base import AsyncBaseRepository, BaseQueryFactory


class SampleItemRepository(
    AsyncBaseRepository[int, SampleItem],
    ABC
):
    """SampleItem repository interface."""


class SampleItemQueryFactory(
    BaseQueryFactory[SampleItem],
    ABC
):
    """SampleItem query."""


class SampleItemByUUIDRepository(
    AsyncBaseRepository[str, SampleItem],
    ABC
):
    """SampleItem repository interface."""
