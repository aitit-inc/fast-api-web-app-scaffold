"""SampleItem controller."""
from typing import Callable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.sample_item.create import \
    SampleItemCreateUseCase
from app.application.use_cases.sample_item.get import SampleItemWithMeta, \
    SampleItemGetUseCase
from app.application.use_cases.sample_item.list import SampleItemListUseCase
from app.application.use_cases.sample_item.logical_delete import \
    SampleItemLogicalDeleteUseCase
from app.application.use_cases.sample_item.physical_delete import \
    SampleItemPhysicalDeleteUseCase
from app.application.use_cases.sample_item.update import \
    SampleItemUpdateUseCase
from app.domain.entities.sample_item import SampleItem, SampleItemCreate, \
    SampleItemRead, SampleItemUpdate
from app.domain.repositories.sample_item import SampleItemRepository
from app.interfaces.views.json_response import ErrorJsonResponse

router = APIRouter(
    prefix='/sample-items',
    tags=['sample-items'],
)


@router.get('/', responses={400: {'model': ErrorJsonResponse}})
@inject
async def sample_item(
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> Page[SampleItem]:
    """
    Retrieve a paginated list of SampleItem entities.

    This GET endpoint uses the SampleItem repository and the
    SampleItemListUseCase to fetch and return a paginated list of
    SampleItem entities.

    Args:
        session_factory (Callable[[], AsyncSession]): An asynchronous
            session factory for creating database sessions.
            Injected as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance 
            using the provided database session. Injected as a dependency.

    Returns:
        Page[SampleItem]: A paginated list of SampleItem entities.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)

            return await SampleItemListUseCase(
                repository
            )()


@router.get('/{entity_id}')
@inject
async def sample_item_by_id(
        entity_id: int,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> SampleItemWithMeta:
    """
    Retrieve a specific SampleItem entity by its ID.

    This GET endpoint uses the SampleItem repository and the
    SampleItemGetUseCase to fetch a single SampleItem entity,
    along with its metadata, based on the provided item ID.

    Args:
        entity_id (int): The identifier of the SampleItem to retrieve.
        session_factory (Callable[[], AsyncSession]): 
            An asynchronous session factory 
            for creating database sessions. Injected as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance
            using the provided database session. Injected as a dependency.

    Returns:
        SampleItemWithMeta: 
            A data structure containing the fetched SampleItem entity 
            along with its metadata.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)

            return await SampleItemGetUseCase(
                repository
            )(entity_id)


@router.post('/', response_model=SampleItemRead,
             status_code=201, )
@inject
async def create_sample_item(
        data: SampleItemCreate,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> SampleItemRead:
    """
    Create a new SampleItem entity.

    This POST endpoint uses the SampleItem repository and the 
    SampleItemCreateUseCase to create a new SampleItem entity based on 
    the provided input data.

    Args:
        data (SampleItemCreate): Data to create the new SampleItem entity.
        session_factory (Callable[[], AsyncSession]): An asynchronous
            session factory for creating database sessions.
            Injected as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance
            using the provided database session. Injected as a dependency.

    Returns:
        SampleItemRead: The created SampleItem entity serialized into a
            `SampleItemRead` format.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)

            entity = await SampleItemCreateUseCase(
                repository
            )(data)

            return SampleItemRead.model_validate(entity)


@router.put('/{entity_id}', response_model=SampleItemRead)
@inject
async def update_sample_item(
        entity_id: int,
        data: SampleItemUpdate,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> SampleItemRead:
    """
    Update an existing SampleItem entity by its ID.

    This PUT endpoint leverages the SampleItem repository and the
    SampleItemUpdateUseCase to update an existing SampleItem entity
    with the new data provided.

    Args:
        entity_id (int): The identifier of the SampleItem to be updated.
        data (SampleItemUpdate):
            The new data with which to update the SampleItem entity.
        session_factory (Callable[[], AsyncSession]):
            An asynchronous session factory
            for creating database sessions. Injected as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance
            using the provided database session. Injected as a dependency.

    Returns:
        SampleItemRead: The updated SampleItem entity serialized into
            a `SampleItemRead` format.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)
            entity = await SampleItemUpdateUseCase(
                repository
            )(entity_id, data)

            return SampleItemRead.model_validate(entity)


@router.delete('/{entity_id}', status_code=204, )
@inject
async def logical_delete_sample_item(
        entity_id: int,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> None:
    """
    Logically delete a specific SampleItem entity by its ID.

    This DELETE endpoint utilizes the SampleItem repository and the
    SampleItemLogicalDeleteUseCase to perform a logical deletion of
    the given SampleItem entity (e.g., marking it as deleted without
    removing it from the database).

    Args:
        entity_id (int): The identifier of the SampleItem to logically delete.
        session_factory (Callable[[], AsyncSession]):
            An asynchronous session factory
            for creating database sessions. Injected as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance
            using the provided database session. Injected as a dependency.

    Returns:
        None: No content is returned from this endpoint.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)
            await SampleItemLogicalDeleteUseCase(
                repository
            )(entity_id)


@router.delete('/{entity_id}/physical', status_code=204, )
@inject
async def physical_delete_sample_item(
        entity_id: int,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> None:
    """
    Physically delete a specific SampleItem entity by its ID.

    This DELETE endpoint uses the SampleItem repository and the
    SampleItemPhysicalDeleteUseCase to permanently delete the given
    SampleItem entity from the database.

    Args:
        entity_id (int): The identifier of the SampleItem to physically delete.
        session_factory (Callable[[], AsyncSession]): An asynchronous
            session factory for creating database sessions. Injected
            as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance
            using the provided database session. Injected as a dependency.
        session_factory (Callable[[], AsyncSession]): An asynchronous
            session factory for creating database sessions. Injected
            as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance
            using the provided database session. Injected as a dependency.
        session_factory (Callable[[], AsyncSession]): An asynchronous
            session factory for creating database sessions. Injected
            as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance
            using the provided database session. Injected as a dependency.

    Returns:
        None: No content is returned from this endpoint.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)
            await SampleItemPhysicalDeleteUseCase(
                repository
            )(entity_id)
