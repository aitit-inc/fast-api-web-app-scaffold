"""SampleItem repository in DB"""
from datetime import datetime
from logging import getLogger
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.sample_item import SampleItemRepository, \
    SampleItemQueryFactory, SampleItemByUUIDRepository
from app.infrastructure.repositories.base import InDBBaseQueryFactory, \
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
    InDBBaseQueryFactory[SampleItem]):
    """In-DB SampleItem query."""
    _entity_cls = SampleItem


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
