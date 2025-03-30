"""SampleItem by UUID controller"""
from typing import Callable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.sample_item import SampleItemGetQuery, \
    SampleItemReadDtoWithMeta, SampleItemReadDto
from app.application.use_cases.sample_item.by_uuid.get import \
    SampleItemGetByUUIDUseCase
from app.domain.repositories.sample_item import SampleItemByUUIDRepository
from app.interfaces.controllers.v1.path import SAMPLE_ITEMS_BY_UUID_PREFIX, \
    PUBLIC_PATH

router = APIRouter(
    prefix=f'{PUBLIC_PATH}{SAMPLE_ITEMS_BY_UUID_PREFIX}',
    tags=['sample-items-by-uuid'],
)


@router.get('/{entity_id}')
@inject
async def sample_item_by_uuid(
        entity_id: str,
        query: SampleItemGetQuery = Depends(),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], SampleItemByUUIDRepository] = Depends(
            Provide['sample_item_by_uuid_repository'])
) -> SampleItemReadDtoWithMeta | SampleItemReadDto:
    """
    Fetch a specific SampleItem entity by its UUID.
    
    Args:
        entity_id (str): The UUID of the SampleItem entity to fetch.
        query (SampleItemGetQuery): Query parameters for retrieving the item,
            provided by FastAPI's dependency injection.
        session_factory (Callable[[], AsyncSession]): A factory function to
            create a new database session, injected via DI.
        repository_factory
            (Callable[[AsyncSession], SampleItemByUUIDRepository]):
            A factory function to create the repository for accessing
            SampleItem data, injected via DI.
    
    Returns:
        SampleItemReadDtoWithMeta | SampleItemReadDto: The requested
            SampleItem entity data, either with metadata or as a plain data
            transfer object.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)

            use_case = SampleItemGetByUUIDUseCase(repository)
            read_data = await use_case(entity_id, query, None)

            return read_data
