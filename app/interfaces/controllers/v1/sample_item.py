"""SampleItem controller."""
from typing import Callable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.sample_item.create import \
    SampleItemCreateUseCase
from app.application.use_cases.sample_item.get import SampleItemGetUseCase
from app.application.use_cases.sample_item.list import \
    SampleItemListUseCase
from app.application.use_cases.sample_item.logical_delete import \
    SampleItemLogicalDeleteUseCase
from app.application.use_cases.sample_item.physical_delete import \
    SampleItemPhysicalDeleteUseCase
from app.application.use_cases.sample_item.update import \
    SampleItemUpdateUseCase
from app.domain.entities.sample_item import SampleItemCreate, \
    SampleItemUpdate
from app.domain.repositories.sample_item import SampleItemRepository, \
    SampleItemQueryFactory
from app.interfaces.serializers.sample_item import sample_item_to_read, \
    sample_item_with_meta_to_read, sample_item_list_transformer, \
    sample_item_with_meta_list_transformer, SampleItemReadWithMeta, \
    SampleItemRead, SampleItemApiListQueryDto
from app.interfaces.views.json_response import ErrorJsonResponse

router = APIRouter(
    prefix='/sample-items',
    tags=['sample-items'],
)


@router.get('/', responses={400: {'model': ErrorJsonResponse}})
@inject
async def sample_item(
        with_meta: bool = False,
        queries: SampleItemApiListQueryDto = Depends(),
        params: Params = Depends(),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        sample_item_query_factory: SampleItemQueryFactory = Depends(
            Provide['sample_item_query_factory']),
) -> Page[SampleItemRead] | Page[SampleItemReadWithMeta]:
    """
    Retrieve a paginated list of SampleItem entities.

    This GET endpoint returns a paginated list of SampleItem entities,
    optionally including metadata.

    Args:
        with_meta (bool): Whether to include metadata in the response.
        queries (SampleItemApiListQueryDto): Query parameters for filtering and
            sorting the SampleItem entities. Injected as a dependency.
        params (Params): Pagination parameters. Injected as a dependency.
        session_factory (Callable[[], AsyncSession]): Factory to create
            database sessions. Injected as a dependency.
        sample_item_query_factory (SampleItemQueryFactory): Factory to
            create SampleItemQuery instances. Injected as a dependency.

    Returns:
        Page[SampleItem] | Page[SampleItemReadWithMeta]: A paginated list of
            SampleItem entities, with or without metadata.
    """
    use_case = SampleItemListUseCase(sample_item_query_factory)
    stmt = use_case(queries.to_domain())

    transformer = sample_item_with_meta_list_transformer \
        if with_meta else sample_item_list_transformer

    async with session_factory() as db_session:
        async with db_session.begin():
            return await paginate(  # type: ignore
                db_session,
                stmt,
                transformer=transformer,
                params=params,
            )


@router.get('/{entity_id}')
@inject
async def sample_item_by_id(
        entity_id: int,
        with_meta: bool = False,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> SampleItemRead | SampleItemReadWithMeta:
    """
    Fetch a specific SampleItem entity by its ID.
    
    Args:
        entity_id (int): The ID of the SampleItem to retrieve.
        with_meta (bool): Whether to include metadata in the response.
        session_factory (Callable[[], AsyncSession]): Factory to create
            database sessions. Injected as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            Factory to create a SampleItemRepository instance. Injected
            as a dependency.
    
    Returns:
        SampleItem | SampleItemReadWithMeta: The fetched SampleItem entity,
        optionally including metadata.
    """
    adapter = sample_item_with_meta_to_read \
        if with_meta else sample_item_to_read

    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)

            use_case = SampleItemGetUseCase(repository)
            entity = await use_case(entity_id)

            return adapter(entity)


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

    This deletes endpoint utilizes the SampleItem repository and the
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

    This deletes endpoint uses the SampleItem repository and the
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
