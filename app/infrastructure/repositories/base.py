"""Repository implementation base class."""
from datetime import datetime
from logging import getLogger
from typing import Generic, Any, Callable

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exc import EntityNotFound
from app.domain.repositories.base import EntityT, AsyncBaseRepository, IdT, \
    UpdateT, BaseQueryFactory
from app.domain.value_objects.api_query import ApiListQuery, \
    ApiListQueryOp

logger = getLogger('uvicorn')


class InDBBaseEntityRepository(
    AsyncBaseRepository[IdT, EntityT],
    Generic[IdT, EntityT],
):
    """Base repository for in-database entities."""
    _entity_cls: type[EntityT]
    _id_field: str = 'id'
    _deleted_at_field: str = 'deleted_at'

    def __init__(
            self,
            db_session: AsyncSession,
            get_now: Callable[[], datetime],
    ):
        """Constructor."""
        self._db_session = db_session
        self._get_now = get_now

    @property
    def id_field(self) -> str:
        """Get the ID field name."""
        return type(self)._id_field

    async def get_by_id(self, entity_id: IdT, *args: Any,
                        include_deleted: bool = False, **kwargs: Any,
                        ) -> EntityT | None:
        """Retrieve an entity by its ID"""
        where_clauses = [
            getattr(self._entity_cls, self.id_field) == entity_id]
        if not include_deleted:
            where_clauses.append(
                getattr(self._entity_cls,
                        self._deleted_at_field).is_(None))
        stmt = select(self._entity_cls).where(*where_clauses)
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, entity: EntityT, *args: Any, **kwargs: Any,
                  ) -> EntityT:
        """Add an entity"""
        self._db_session.add(entity)
        await self._db_session.flush()
        await self._db_session.refresh(entity)
        return entity

    async def update(self, entity_id: IdT, data: UpdateT,
                     *args: Any, **kwargs: Any,
                     ) -> EntityT:
        """Update an entity"""
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

    async def logical_delete(self, entity_id: IdT,
                             *args: Any, **kwargs: Any,
                             ) -> None:
        """Logical delete the entity with the specified ID."""
        existing_entity = await self.get_by_id(entity_id)
        if existing_entity:
            setattr(existing_entity, self._deleted_at_field, self._get_now())
            await self._db_session.merge(existing_entity)
            await self._db_session.flush()
        else:
            logger.warning('Entity with ID %s does not exist.', entity_id)

    async def delete(self, entity_id: IdT,
                     *args: Any, **kwargs: Any,
                     ) -> None:
        """Delete the entity with the specified ID."""
        existing_entity = await self.get_by_id(entity_id)
        if existing_entity:
            await self._db_session.delete(existing_entity)
            await self._db_session.flush()
        else:
            logger.warning('Entity with ID %s does not exist.', entity_id)


class InDBBaseQueryFactory(
    BaseQueryFactory[EntityT],
    Generic[EntityT],
):
    """Base query factory for in-database repositories."""
    _entity_cls: type[EntityT]
    _deleted_at_field: str = 'deleted_at'

    def list_query(
            self,
            api_query: ApiListQuery,
            *args: Any,
            **kwargs: Any,
    ) -> Select[tuple[EntityT]]:
        """list query."""
        return self._list_query(api_query, self._entity_cls)

    def _list_query(
            self,
            api_query: ApiListQuery,
            model: type[EntityT],
            include_deleted: bool = False,
    ) -> Select[tuple[EntityT]]:
        """Private method for constructing the list query."""
        stmt = select(model)
        queries = api_query.queries

        if not include_deleted:
            stmt = stmt.where(
                getattr(model, self._deleted_at_field).is_(None))

        def _get_field_op(key_: str) -> tuple[str, str]:
            field_, op_ = key_.split('__')
            return field_, op_

        # operation mapping
        filter_operations = {
            ApiListQueryOp.EQ: lambda field_, value_: field_ == value_,
            ApiListQueryOp.NEQ: lambda field_, value_: field_ != value_,
            ApiListQueryOp.LIKE: lambda field_, value_: field_.ilike(value_),
            ApiListQueryOp.GT: lambda field_, value_: field_ > value_,
            ApiListQueryOp.GTE: lambda field_, value_: field_ >= value_,
            ApiListQueryOp.LT: lambda field_, value_: field_ < value_,
            ApiListQueryOp.LTE: lambda field_, value_: field_ <= value_,
            ApiListQueryOp.IN: lambda field_, value_: field_.in_(value_),
            ApiListQueryOp.NOTIN: lambda field_, value_: field_.notin_(value_),
        }

        for key, value in queries.items():
            # Filter query
            field, op = _get_field_op(key)
            field_obj = getattr(model, field)
            if op in filter_operations:
                stmt = stmt.where(
                    filter_operations[op](field_obj, value))  # type: ignore

        sort_operations = {
            ApiListQueryOp.ASC: lambda field_: field_,
            ApiListQueryOp.DESC: lambda field_: field_.desc(),
        }

        for key, value in queries.items():
            # Sort query
            field, op = _get_field_op(key)
            if op in sort_operations and value is True:
                stmt = stmt.order_by(
                    sort_operations[op](getattr(model, field)))  # type: ignore

        return stmt
