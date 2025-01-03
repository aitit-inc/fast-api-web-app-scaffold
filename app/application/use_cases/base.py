"""Base class of application use cases."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Sequence, Callable

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exc import EntityNotFound
from app.domain.repositories.base import AsyncBaseRepository, BaseQueryFactory

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


ReturnT = TypeVar('ReturnT')
IdT = TypeVar('IdT', int, str)
EntityT = TypeVar('EntityT')
CreateT = TypeVar('CreateT')
UpdateT = TypeVar('UpdateT')


class AsyncBaseListUseCase(
    AsyncBaseUseCase[Page[ReturnT]],
    Generic[ReturnT, IdT, EntityT, CreateT, UpdateT]
):
    """Async list use case base class."""

    def __init__(
            self,
            db_session: AsyncSession,
            query_factory: BaseQueryFactory[EntityT],
    ) -> None:
        """Constructor."""
        self._db_session = db_session
        self._query_factory = query_factory

    async def __call__(
            self,
            params: Params,
    ) -> Page[ReturnT]:
        """Execute the use case."""
        stmt = self._query_factory.list_query()

        return await paginate(  # type: ignore
            self._db_session,
            stmt,
            transformer=self.transform(),
            params=params,
        )

    @staticmethod
    @abstractmethod
    def transform() -> Callable[[Sequence[EntityT]], Sequence[ReturnT]]:
        """Transform or process the retrieved entity."""


class AsyncBaseListEntityUseCase(
    AsyncBaseListUseCase[EntityT, IdT, EntityT, CreateT, UpdateT],
    Generic[IdT, EntityT, CreateT, UpdateT],
):
    """Async list use case base class."""

    @staticmethod
    def transform() -> Callable[[Sequence[EntityT]], Sequence[EntityT]]:
        def transformer(xs: Sequence[EntityT]) -> Sequence[EntityT]:
            adapter = TypeAdapter(list[EntityT])
            return adapter.validate_python(xs)

        return transformer


class AsyncBaseGetUseCase(
    AsyncBaseUseCase[ReturnT],
    Generic[ReturnT, IdT, EntityT, CreateT, UpdateT],
    ABC
):
    """Async get use case base class."""

    def __init__(
            self,
            repository: AsyncBaseRepository[
                IdT, EntityT, CreateT, UpdateT
            ]) -> None:
        """Constructor."""
        self._repository: AsyncBaseRepository[
            IdT, EntityT, CreateT, UpdateT] = repository

    async def __call__(
            self,
            entity_id: IdT,
            *args: Any,
            **kwargs: Any,
    ) -> ReturnT:
        """Execute the use case."""
        entity = await self._repository.get_by_id(entity_id)
        if not entity:
            raise EntityNotFound(
                EntityNotFound.to_msg(entity_id),
                detail=f'Entity with ID {entity_id} does not exist.'
            )

        return self.transform(entity)

    @abstractmethod
    def transform(self, entity: EntityT) -> ReturnT:
        """Transform or process the retrieved entity."""


class AsyncBaseGetEntityUseCase(
    AsyncBaseGetUseCase[EntityT, IdT, EntityT, CreateT, UpdateT],
    Generic[IdT, EntityT, CreateT, UpdateT],
):
    """Async get entity use case base class."""

    def transform(self, entity: EntityT) -> EntityT:
        """Transform or process the retrieved entity."""
        return entity


class AsyncBaseCreateUseCase(
    AsyncBaseUseCase[EntityT],
    Generic[IdT, EntityT, CreateT, UpdateT]
):
    """Async create use case base class."""

    def __init__(
            self,
            repository: AsyncBaseRepository[
                IdT, EntityT, CreateT, UpdateT
            ]) -> None:
        """Constructor."""
        self._repository: AsyncBaseRepository[
            IdT, EntityT, CreateT, UpdateT] = repository

    async def __call__(
            self,
            data: CreateT,
            *args: Any,
            **kwargs: Any,
    ) -> EntityT:
        """Execute the use case."""
        return await self._repository.add(data)
