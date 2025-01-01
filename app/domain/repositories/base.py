"""Base repository interface for managing domain entities."""
from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Any

from fastapi_pagination import Page

# A generic type variable representing the type of entities
EntityT = TypeVar('EntityT')
CreateT = TypeVar('CreateT')
UpdateT = TypeVar('UpdateT')
IdT = TypeVar('IdT')

FiltersType = dict[str, Any] | None


class AsyncBaseRepository(
    ABC,
    Generic[IdT, EntityT, CreateT, UpdateT],
):
    """Async base repository interface for managing domain entities."""

    @abstractmethod
    async def get_list(
            self, filters: FiltersType = None) -> Page[EntityT]:
        """Retrieve a list of entities, optionally filtered by the given criteria."""

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
