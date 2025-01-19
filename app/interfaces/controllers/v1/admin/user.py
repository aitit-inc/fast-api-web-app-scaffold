"""User controller."""
from typing import Callable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user import UserApiListQueryDto, UserReadDto, \
    UserCreate
from app.application.use_cases.user.common import user_list_transformer
from app.application.use_cases.user.create import UserCreateUseCase
from app.application.use_cases.user.list import UserListUseCase
from app.domain.repositories.user import UserQueryFactory, UserByUUIDRepository
from app.domain.services.auth import UserAuthService
from app.interfaces.views.json_response import ErrorJsonResponse

router = APIRouter(
    prefix='/admin/users',
    tags=['admin-users'],
)


@router.get('/', responses={400: {'model': ErrorJsonResponse}})
@inject
async def users(
        query: UserApiListQueryDto = Depends(),
        params: Params = Depends(),
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        user_query_factory: UserQueryFactory = Depends(
            Provide['user_query_factory']),
) -> Page[UserReadDto]:
    """
    Retrieves a paginated list of users based on the query parameters provided.
    
    Args:
        query (UserApiListQueryDto): The query data transfer object for
            filtering users.
        params (Params): Pagination parameters such as page size and number.
        session_factory (Callable[[], AsyncSession]): A factory function to
            create an asynchronous SQLAlchemy session.
        user_query_factory (UserQueryFactory): Factory for constructing user
            queries.
    
    Returns:
        Page[UserReadDto]: A paginated list of users represented as
            UserReadDto instances.
    """
    use_case = UserListUseCase(user_query_factory)
    stmt = use_case(query)

    async with session_factory() as db_session:
        async with db_session.begin():
            return await paginate(  # type: ignore
                db_session,
                stmt,
                transformer=user_list_transformer,
                params=params,
            )


@router.post('/', status_code=201,
             responses={400: {'model': ErrorJsonResponse}})
@inject
async def create_user(
        data: UserCreate,
        session_factory: Callable[[], AsyncSession] = Depends(
            Provide['db_session_factory']),
        repository_factory: Callable[
            [AsyncSession], UserByUUIDRepository] = Depends(
            Provide['user_by_uuid_repository']),
        user_auth_service_factory: Callable[
            [UserByUUIDRepository], UserAuthService] = Depends(
            Provide['user_auth_service_factory']),
) -> UserReadDto:
    """
    Creates a new user in the database.

    Args:
        data (UserCreate): DTO containing the user creation request payload.
        session_factory (Callable[[], AsyncSession]): Factory function to
            create an async SQLAlchemy session.
        repository_factory (Callable[[AsyncSession], UserByUUIDRepository]):
            Factory to obtain the user repository.
        user_auth_service_factory
            (Callable[[UserByUUIDRepository], UserAuthService]):
            Factory to obtain the user auth service.

    Returns:
        UserReadDto: The newly created user data.

    Raises:
        HTTPException: If there is any error during user creation.
    """
    async with session_factory() as db_session:
        async with db_session.begin():
            repository = repository_factory(db_session)
            user_auth_service = user_auth_service_factory(repository)

            use_case = UserCreateUseCase(repository, user_auth_service)
            read_data = await use_case(data, None)

            return read_data
