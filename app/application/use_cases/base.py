"""Base class of application use cases."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

from pydantic import BaseModel
from sqlalchemy import Select

from app.application.exc import EntityNotFound
from app.domain.repositories.base import BaseQueryFactory, \
    AsyncBaseRepository
from app.domain.value_objects.api_query import ApiListQuery

T = TypeVar('T')


class BaseUseCase(Generic[T], ABC):
    """
    Base class for all application use cases.

    This class should be inherited by all use case classes
    to enforce a common structure and behavior.
    """

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """
        Execute the use case. Subclasses must implement this method.
        """


class AsyncBaseUseCase(Generic[T], ABC):
    """
    Async base class for all application use cases.

    This class should be inherited by asynchronous use case classes
    to enforce a common structure and behavior.
    """

    @abstractmethod
    async def __call__(self, *args: Any, **kwargs: Any) -> T:
        """
        Execute the async use case. Subclasses must implement this method.
        """


IdT = TypeVar('IdT', int, str)
EntityT = TypeVar('EntityT', bound=BaseModel)
UpdateT = TypeVar('UpdateT', bound=BaseModel)
RepositoryT = TypeVar('RepositoryT', bound=AsyncBaseRepository[
    IdT, EntityT, UpdateT])


class BaseListUseCase(
    BaseUseCase[Select[tuple[EntityT]]],
    Generic[EntityT],
):
    """Async list use case base class."""

    def __init__(
            self,
            query_factory: BaseQueryFactory[EntityT],
    ) -> None:
        """Constructor."""
        self._query_factory = query_factory

    def __call__(self, api_query: ApiListQuery) -> Select[tuple[EntityT]]:
        return self._query_factory.list_query(api_query)


class AsyncBaseGetUseCase(
    AsyncBaseUseCase[EntityT],
    Generic[IdT, EntityT, RepositoryT],
    ABC
):
    """Async get use case base class."""

    def __init__(
            self,
            repository: RepositoryT,
    ) -> None:
        """Constructor."""
        self._repository = repository

    async def __call__(
            self,
            entity_id: IdT,
            *args: Any,
            **kwargs: Any,
    ) -> EntityT:
        """Execute the use case."""
        entity: EntityT | None = await self._repository.get_by_id(entity_id)
        if not entity:
            raise EntityNotFound(
                EntityNotFound.to_msg(entity_id),
                detail=f'Entity with ID {entity_id} does not exist.'
            )

        return entity


class AsyncBaseCreateUseCase(
    AsyncBaseUseCase[EntityT],
    Generic[IdT, EntityT, RepositoryT]
):
    """Async create use case base class."""

    def __init__(
            self,
            repository: RepositoryT,
    ) -> None:
        """Constructor."""
        self._repository: RepositoryT = repository

    async def __call__(
            self,
            entity: EntityT,
            *args: Any,
            **kwargs: Any,
    ) -> EntityT:
        """Execute the use case."""
        created_entity: EntityT = await self._repository.add(entity)

        return created_entity
