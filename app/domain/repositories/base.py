"""Base repository interface for managing domain entities."""
from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Any

from sqlalchemy.sql.selectable import Select

# A generic type variable representing the type of entities
IdT = TypeVar('IdT')
EntityT = TypeVar('EntityT')
CreateT = TypeVar('CreateT')
UpdateT = TypeVar('UpdateT')

FiltersType = dict[str, Any] | None


class AsyncBaseRepository(
    Generic[IdT, EntityT, CreateT, UpdateT],
    ABC
):
    """Async base repository interface for managing domain entities."""

    @abstractmethod
    async def get_by_id(self, entity_id: IdT) -> EntityT | None:
        """Retrieve an entity by its ID"""

    @abstractmethod
    async def add(self, data: CreateT) -> EntityT:
        """Add an entity"""

    @abstractmethod
    async def update(self, entity_id: IdT, data: UpdateT) -> EntityT:
        """Update an entity"""

    @abstractmethod
    async def logical_delete(self, entity_id: IdT) -> None:
        """Logical delete an entity by its ID"""

    @abstractmethod
    async def delete(self, entity_id: IdT) -> None:
        """Delete an entity by its ID"""


class BaseQueryFactory(
    Generic[EntityT],
    ABC
):
    """Base query factory interface."""

    @abstractmethod
    def list_query(self, *args: Any, **kwargs: Any) -> Select[tuple[EntityT]]:
        """Construct a SQL query for retrieving a list of entities."""
