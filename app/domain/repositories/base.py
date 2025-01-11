"""Base repository interface for managing domain entities."""
from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Any

from sqlalchemy import Select
from sqlmodel import SQLModel

from app.domain.value_objects.api_query import ApiListQuery

# A generic type variable representing the type of entities
IdT = TypeVar('IdT', int, str)
EntityT = TypeVar('EntityT', bound=SQLModel)
UpdateT = dict[str, Any]

FiltersType = dict[str, Any] | None


class AsyncBaseRepository(
    Generic[IdT, EntityT],
    ABC
):
    """Async base repository interface for managing domain entities."""

    @abstractmethod
    async def get_by_id(self, entity_id: IdT) -> EntityT | None:
        """Retrieve an entity by its ID"""

    @abstractmethod
    async def add(self, entity: EntityT) -> EntityT:
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
    def list_query(
            self,
            api_query: ApiListQuery,
            *args: Any,
            **kwargs: Any
    ) -> Select[tuple[EntityT]]:
        """Construct a SQL query for retrieving a list of entities."""
