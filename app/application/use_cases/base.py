"""Base class of application use cases."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

from pydantic import BaseModel
from sqlalchemy import Select
from sqlmodel import SQLModel

from app.application.exc import EntityNotFound
from app.domain.repositories.base import BaseQueryFactory, \
    AsyncBaseRepository
from app.application.dto.base import ApiListQueryDtoBaseModel

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
ApiQueryT = TypeVar('ApiQueryT', bound=ApiListQueryDtoBaseModel | None)
ApiBodyT = TypeVar('ApiBodyT', bound=BaseModel | None)
EntityT = TypeVar('EntityT', bound=BaseModel | SQLModel)
CreateT = TypeVar('CreateT', bound=BaseModel | SQLModel)
UpdateT = TypeVar('UpdateT', bound=BaseModel | SQLModel)
ReturnT = TypeVar('ReturnT', bound=BaseModel | SQLModel)
RepositoryT = TypeVar('RepositoryT', bound=AsyncBaseRepository[
    IdT, EntityT])


class BaseListUseCase(
    BaseUseCase[Select[tuple[EntityT]]],
    Generic[ApiQueryT, EntityT],
):
    """Async list use case base class."""

    def __init__(
            self,
            query_factory: BaseQueryFactory[EntityT],
    ) -> None:
        """Constructor."""
        self._query_factory = query_factory

    def __call__(self, api_query: ApiQueryT) -> Select[tuple[EntityT]]:
        return self._query_factory.list_query(api_query.to_domain())


class AsyncBaseGetByIdUseCase(
    AsyncBaseUseCase[ReturnT],
    Generic[IdT, ApiQueryT, ApiBodyT, EntityT, ReturnT, RepositoryT],
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
            query: ApiQueryT,
            body: ApiBodyT,
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

        return self._to_return_dto(entity, query, body)

    @abstractmethod
    def _to_return_dto(
            self,
            entity: EntityT,
            query: ApiQueryT,
            body: ApiBodyT,
    ) -> ReturnT:
        """Convert an EntityT to a ReturnDTO."""


class AsyncBaseCreateUseCase(
    AsyncBaseUseCase[ReturnT],
    Generic[ApiQueryT, EntityT, CreateT, ReturnT, RepositoryT],
    ABC
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
            dto: CreateT,
            query: ApiQueryT,
            *args: Any,
            **kwargs: Any,
    ) -> ReturnT:
        """Execute the use case."""
        entity = self._from_create_dto(dto, query)
        created_entity = await self._repository.add(entity)

        return self._to_return_dto(created_entity, query)

    @abstractmethod
    def _from_create_dto(self, dto: CreateT, query: ApiQueryT) -> EntityT:
        """Convert a CreateDTO to an EntityT."""

    @abstractmethod
    def _to_return_dto(self, entity: EntityT, query: ApiQueryT) -> ReturnT:
        """Convert an EntityT to a ReturnDTO."""


class AsyncBaseUpdateUseCase(
    AsyncBaseUseCase[ReturnT],
    Generic[IdT, ApiQueryT, EntityT, UpdateT, ReturnT, RepositoryT],
    ABC
):
    """Async update use case base class."""

    def __init__(
            self,
            repository: RepositoryT,
    ) -> None:
        """Constructor."""
        self._repository: RepositoryT = repository

    async def __call__(
            self,
            entity_id: IdT,
            dto: UpdateT,
            query: ApiQueryT,
            *args: Any,
            **kwargs: Any,
    ) -> ReturnT:
        """Execute the use case."""
        data = self._from_update_dto(dto, query)
        updated_entity = await self._repository.update(entity_id, data)

        return self._to_return_dto(updated_entity, query)

    @abstractmethod
    def _from_update_dto(
            self, dto: UpdateT, query: ApiQueryT) -> dict[str, Any]:
        """Convert an UpdateDTO to a dict."""

    @abstractmethod
    def _to_return_dto(self, entity: EntityT, query: ApiQueryT) -> ReturnT:
        """Convert an EntityT to a ReturnDTO."""


class AsyncBaseLogicalDeleteUseCase(
    AsyncBaseUseCase[None],
    Generic[IdT, RepositoryT],
    ABC
):
    """Async logical delete use case base class."""

    def __init__(
            self,
            repository: RepositoryT,
    ) -> None:
        """Constructor."""
        self._repository: RepositoryT = repository

    async def __call__(
            self,
            entity_id: IdT,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        """Execute the use case."""
        await self._repository.logical_delete(entity_id)


class AsyncBasePhysicalDeleteUseCase(
    AsyncBaseUseCase[None],
    Generic[IdT, RepositoryT],
    ABC
):
    """Async physical delete use case base class."""

    def __init__(
            self,
            repository: RepositoryT,
    ) -> None:
        """Constructor."""
        self._repository: RepositoryT = repository

    async def __call__(
            self,
            entity_id: IdT,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        """Execute the use case."""
        await self._repository.delete(entity_id)
