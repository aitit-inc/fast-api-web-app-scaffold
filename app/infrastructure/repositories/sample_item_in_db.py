"""SampleItem repository in DB"""
from datetime import datetime
from logging import getLogger
from typing import Callable, Any

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.sample_item import SampleItemRepository, \
    SampleItemQueryFactory, SampleItemByUUIDRepository
from app.domain.value_objects.api_query import ApiListQuery
from app.infrastructure.repositories.base import InDBQueryFactoryTrait, \
    InDBBaseEntityRepository

logger = getLogger('uvicorn')


class InDBSampleItemRepository(
    SampleItemRepository,
    InDBBaseEntityRepository[int, SampleItem],
):
    """In-DB SampleItem repository."""
    _entity_cls = SampleItem

    @staticmethod
    def factory(
            get_now: Callable[[], datetime]
    ) -> Callable[[AsyncSession], 'InDBSampleItemRepository']:
        """Factory method."""
        return lambda db_session: InDBSampleItemRepository(db_session, get_now)


class InDBSampleItemQueryFactory(
    SampleItemQueryFactory,
    InDBQueryFactoryTrait[SampleItem]):
    """In-DB SampleItem query."""

    def list_query(
            self,
            api_query: ApiListQuery,
            *args: Any,
            **kwargs: Any,
    ) -> Select[tuple[SampleItem]]:
        """list query."""
        return self._list_query(api_query, SampleItem)


class InDBSampleItemByUUIDRepository(
    SampleItemByUUIDRepository,
    InDBBaseEntityRepository[str, SampleItem],
):
    """In-DB SampleItem repository by UUID."""
    _entity_cls = SampleItem
    _id_field = 'uuid'

    @staticmethod
    def factory(
            get_now: Callable[[], datetime]
    ) -> Callable[[AsyncSession], 'InDBSampleItemByUUIDRepository']:
        """Factory method."""
        return lambda db_session: InDBSampleItemByUUIDRepository(
            db_session, get_now)
