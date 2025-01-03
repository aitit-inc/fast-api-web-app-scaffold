"""Base class of application use cases."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Sequence, Callable

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import TypeAdapter, BaseModel
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


ReturnT = TypeVar('ReturnT', bound=BaseModel)
IdT = TypeVar('IdT', int, str)
EntityT = TypeVar('EntityT', bound=BaseModel)
CreateT = TypeVar('CreateT', bound=BaseModel)
UpdateT = TypeVar('UpdateT', bound=BaseModel)


class AsyncBaseListUseCase(
    AsyncBaseUseCase[Page[ReturnT]],
    Generic[ReturnT, IdT, EntityT, CreateT, UpdateT],
    ABC
):
    """Async list use case base class."""

    def __init__(
            self,
            db_session: AsyncSession,
            query_factory: BaseQueryFactory[EntityT],
            adapter_to_read: Callable[[EntityT], ReturnT],
    ) -> None:
        """Constructor."""
        self._db_session = db_session
        self._query_factory = query_factory
        self._adapter_to_read = adapter_to_read

    async def __call__(
            self,
            params: Params,
    ) -> Page[ReturnT]:
        """Execute the use case."""
        stmt = self._query_factory.list_query()

        return await paginate(  # type: ignore
            self._db_session,
            stmt,
            transformer=self.transformer(),
            params=params,
        )

    def transformer(self) -> Callable[[Sequence[EntityT]], Sequence[ReturnT]]:
        """Transform or process the retrieved entity."""

        def _transformer(xs: Sequence[EntityT]) -> Sequence[ReturnT]:
            transformed = [self._adapter_to_read(x) for x in xs]
            adapter = TypeAdapter(list[ReturnT])
            return adapter.validate_python(transformed)

        return _transformer


class AsyncBaseGetUseCase(
    AsyncBaseUseCase[ReturnT],
    Generic[ReturnT, IdT, EntityT, CreateT, UpdateT],
    ABC
):
    """Async get use case base class."""

    def __init__(
            self,
            repository: AsyncBaseRepository[
                IdT, EntityT, CreateT, UpdateT],
            adapter_to_read: Callable[[EntityT], ReturnT],
    ) -> None:
        """Constructor."""
        self._repository: AsyncBaseRepository[
            IdT, EntityT, CreateT, UpdateT] = repository
        self._adapter_to_read = adapter_to_read

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

        return self._adapter_to_read(entity)


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
