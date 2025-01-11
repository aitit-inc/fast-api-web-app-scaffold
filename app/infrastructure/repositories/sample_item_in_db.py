"""SampleItem repository in DB"""
from datetime import datetime
from logging import getLogger
from typing import Callable, Any

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exc import EntityNotFound
from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.base import UpdateT
from app.domain.repositories.sample_item import SampleItemRepository, \
    SampleItemQueryFactory
from app.domain.value_objects.api_query import ApiListQuery
from app.infrastructure.repositories.base import InDBQueryFactoryTrait

logger = getLogger('uvicorn')


class InDBSampleItemRepository(SampleItemRepository):
    """In-DB SampleItem repository."""

    @staticmethod
    def factory(
            get_now: Callable[[], datetime]
    ) -> Callable[[AsyncSession], 'InDBSampleItemRepository']:
        """Factory method."""
        return lambda db_session: InDBSampleItemRepository(db_session, get_now)

    def __init__(
            self,
            db_session: AsyncSession,
            get_now: Callable[[], datetime],
    ):
        """Constructor."""
        self._db_session = db_session
        self._get_now = get_now

    async def get_by_id(
            self, entity_id: int) -> SampleItem | None:
        """Retrieve an entity by its ID."""
        stmt = select(SampleItem).where(
            SampleItem.id == entity_id)  # type: ignore
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, entity: SampleItem) -> SampleItem:
        """Add an entity."""
        self._db_session.add(entity)
        await self._db_session.flush()
        await self._db_session.refresh(entity)
        return entity

    async def update(self, entity_id: int,
                     data: UpdateT) -> SampleItem:
        """Update an entity."""
        existing_entity = await self.get_by_id(entity_id)
        if not existing_entity:
            raise EntityNotFound(
                EntityNotFound.to_msg(entity_id),
            )

        existing_entity.sqlmodel_update(data)
        await self._db_session.merge(existing_entity)
        await self._db_session.flush()
        await self._db_session.refresh(existing_entity)
        return existing_entity

    async def logical_delete(self, entity_id: int) -> None:
        """Logical delete the entity with the specified ID."""
        existing_entity = await self.get_by_id(entity_id)
        if existing_entity:
            existing_entity.deleted_at = self._get_now()
            await self._db_session.merge(existing_entity)
            await self._db_session.flush()
        else:
            logger.warning('Entity with ID %s does not exist.', entity_id)

    async def delete(self, entity_id: int) -> None:
        """Delete the entity with the specified ID."""
        existing_entity = await self.get_by_id(entity_id)
        if existing_entity:
            await self._db_session.delete(existing_entity)
        else:
            logger.warning('Entity with ID %s does not exist.', entity_id)


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
