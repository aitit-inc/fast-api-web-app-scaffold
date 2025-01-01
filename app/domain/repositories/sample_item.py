"""SampleItem repository interface."""
from abc import ABC

from app.domain.entities.sample_item import SampleItem, SampleItemCreate, \
    SampleItemUpdate
from app.domain.repositories.base import AsyncBaseRepository


# pylint: disable=too-few-public-methods
class SampleItemRepository(
    AsyncBaseRepository[int, SampleItem, SampleItemCreate, SampleItemUpdate],
    ABC
):
    """SampleItem repository interface."""
