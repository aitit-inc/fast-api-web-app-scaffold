"""SampleItem repository in DB"""
from logging import getLogger
from typing import Sequence

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exc import EntityNotFound
from app.domain.entities.sample_item import SampleItem, SampleItemCreate, \
    SampleItemUpdate
from app.domain.repositories.base import FiltersType
from app.domain.repositories.sample_item import SampleItemRepository
from app.infrastructure.mappers.sample_item import sample_item_from_create

logger = getLogger('uvicorn')


class InDBSampleItemRepository(SampleItemRepository):
    """In-DB SampleItem repository."""

    def __init__(self, db_session: AsyncSession):
        """Constructor."""
        self._db_session = db_session

    async def get_list(
            self, filters: FiltersType = None) -> Page[SampleItem]:
        """Retrieve a list of entities,
        optionally filtered by the given criteria."""
        stmt = select(SampleItem)
        if filters:
            filter_conditions = []
            if 'name' in filters:
                filter_conditions.append(SampleItem.name == filters['name'])

            stmt = stmt.where(*filter_conditions)

        def transformer(xs: Sequence[SampleItem]) -> Sequence[SampleItem]:
            adapter = TypeAdapter(list[SampleItem])
            return adapter.validate_python(xs)

        return await paginate(  # type: ignore
            self._db_session,
            stmt,
            transformer=transformer,
        )

    async def get_by_id(
            self, entity_id: int) -> SampleItem | None:
        """Retrieve an entity by its ID."""
        stmt = select(SampleItem).where(
            SampleItem.id == entity_id)  # type: ignore
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, data: SampleItemCreate) -> SampleItem:
        """Add an entity."""
        entity = sample_item_from_create(data)
        self._db_session.add(entity)
        await self._db_session.flush()
        await self._db_session.refresh(entity)
        return entity

    async def update(self, entity_id: int,
                     data: SampleItemUpdate) -> SampleItem:
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
            existing_entity.is_deleted = True
            await self._db_session.merge(existing_entity)
            await self._db_session.flush()
        else:
            logger.warning(f'Entity with ID {entity_id} does not exist.')

    async def delete(self, entity_id: int) -> None:
        """Delete the entity with the specified ID."""
        existing_entity = await self.get_by_id(entity_id)
        if existing_entity:
            await self._db_session.delete(existing_entity)
        else:
            logger.warning(f'Entity with ID {entity_id} does not exist.')
