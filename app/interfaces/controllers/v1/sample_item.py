"""SampleItem controller."""
from typing import Callable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.sample_item import SampleItemUpdateDto, \
    SampleItemCreate, SampleItemReadDto, SampleItemReadDtoWithMeta, \
    SampleItemGetQuery, SampleItemApiListQueryDto
from app.application.use_cases.sample_item.common import \
    sample_item_list_transformer, sample_item_with_meta_list_transformer
from app.application.use_cases.sample_item.create import \
    SampleItemCreateUseCase
from app.application.use_cases.sample_item.get import SampleItemGetByIdUseCase
from app.application.use_cases.sample_item.list import \
    SampleItemListUseCase
from app.application.use_cases.sample_item.logical_delete import \
    SampleItemLogicalDeleteUseCase
from app.application.use_cases.sample_item.physical_delete import \
    SampleItemPhysicalDeleteUseCase
from app.application.use_cases.sample_item.update import \
    SampleItemUpdateUseCase
from app.domain.repositories.sample_item import SampleItemRepository, \
    SampleItemQueryFactory
from app.interfaces.views.json_response import ErrorJsonResponse

router = APIRouter(
    prefix='/sample-items',
    tags=['sample-items'],
)


@router.get('/', responses={400: {'model': ErrorJsonResponse}})
@inject
async def sample_item(
        with_meta: bool = False,
        query: SampleItemApiListQueryDto = Depends(),
        params: Params = Depends(),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        sample_item_query_factory: SampleItemQueryFactory = Depends(
            Provide['sample_item_query_factory']),
) -> Page[SampleItemReadDtoWithMeta] | Page[SampleItemReadDto]:
    """
    Retrieve a paginated list of SampleItem entities.

    This GET endpoint returns a paginated list of SampleItem entities,
    optionally including metadata.

    Args:
        with_meta (bool): Whether to include metadata in the response.
        query (SampleItemApiListQueryDto): Query parameters for filtering and
            sorting the SampleItem entities. Injected as a dependency.
        params (Params): Pagination parameters. Injected as a dependency.
        session_factory (Callable[[], AsyncSession]): Factory to create
            database sessions. Injected as a dependency.
        sample_item_query_factory (SampleItemQueryFactory): Factory to
            create SampleItemQuery instances. Injected as a dependency.

    Returns:
        Page[SampleItem] | Page[SampleItemReadDtoWithMeta]: A paginated list of
            SampleItem entities, with or without metadata.
    """
    use_case = SampleItemListUseCase(sample_item_query_factory)
    stmt = use_case(query)

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
        query: SampleItemGetQuery = Depends(),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> SampleItemReadDtoWithMeta | SampleItemReadDto:
    """
    Fetch a specific SampleItem entity by its ID.
    
    Args:
        entity_id (int): The ID of the SampleItem to retrieve.
        query (SampleItemGetQuery): Query parameters for the SampleItem
            entity. Injected as a dependency.
        session_factory (Callable[[], AsyncSession]): Factory to create
            database sessions. Injected as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            Factory to create a SampleItemRepository instance. Injected
            as a dependency.
    
    Returns:
        SampleItemReadDto | SampleItemReadDtoWithMeta:
            The fetched SampleItem entity, optionally including metadata.
    """

    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)

            use_case = SampleItemGetByIdUseCase(repository)
            read_data = await use_case(entity_id, query, None)

            return read_data


@router.post('/', response_model=SampleItemReadDto,
             status_code=201, )
@inject
async def create_sample_item(
        data: SampleItemCreate,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> SampleItemReadDto:
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
        SampleItemReadDto: The created SampleItem entity serialized into a
            `SampleItemRead` format.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)

            use_case = SampleItemCreateUseCase(repository)
            read_data = await use_case(data, None)

            return read_data


@router.put('/{entity_id}', response_model=SampleItemReadDto)
@inject
async def update_sample_item(
        entity_id: int,
        data: SampleItemUpdateDto,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemRepository] = Depends(
            Provide['sample_item_repository'])
) -> SampleItemReadDto:
    """
    Update an existing SampleItem entity by its ID.

    This PUT endpoint leverages the SampleItem repository and the
    SampleItemUpdateUseCase to update an existing SampleItem entity
    with the new data provided.

    Args:
        entity_id (int): The identifier of the SampleItem to be updated.
        data (SampleItemUpdateDto):
            The new data with which to update the SampleItem entity.
        session_factory (Callable[[], AsyncSession]):
            An asynchronous session factory
            for creating database sessions. Injected as a dependency.
        repository_factory (Callable[[AsyncSession], SampleItemRepository]):
            A callable that initializes a SampleItemRepository instance
            using the provided database session. Injected as a dependency.

    Returns:
        SampleItemReadDto: The updated SampleItem entity serialized into
            a `SampleItemRead` format.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)
            use_case = SampleItemUpdateUseCase(
                repository
            )
            read_data = await use_case(entity_id, data, None)

            return read_data


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
