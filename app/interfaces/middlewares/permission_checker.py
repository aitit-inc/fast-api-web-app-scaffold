"""Permission checker."""
import functools
from logging import getLogger
from typing import Callable, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.application.exc import Forbidden
from app.domain.entities.user import User, Role
from app.domain.repositories.user import UserByUUIDRepository

logger = getLogger('uvicorn')

REQUIRED_PERMISSION_FIELD = '_required_permission'


class PermissionChecker:
    """Permission checker."""

    def __init__(
            self,
            session_factory: Callable[[], AsyncSession],
            user_by_uuid_repository_factory: Callable[
                [AsyncSession], UserByUUIDRepository],
    ):
        self._session_factory = session_factory
        self._user_by_uuid_repository_factory = user_by_uuid_repository_factory

    async def permitted(
            self,
            user_uuid: str,
            required_permission_names: list[str],
    ) -> None:
        """Check permission."""

        async with self._session_factory() as db_session:
            async with db_session.begin():

                user_by_uuid_repository = \
                    self._user_by_uuid_repository_factory(db_session)
                user = await user_by_uuid_repository.get_by_id(
                    user_uuid,
                    load_options=[
                        joinedload(
                            User.roles  # type: ignore
                        ).joinedload(
                            Role.permissions)]  # type: ignore
                )
                if user is None:
                    logger.warning(
                        'User not found by UUID: %s', user_uuid)
                    raise Forbidden('Missing permission')

                # superuser has full access permission.
                if user.is_superuser:
                    return

                roles = user.roles
                user_permission_names = set(sum([
                    [permission.name for permission in role.permissions
                     ] for role in roles], []))

                if not user_permission_names & set(required_permission_names):
                    logger.warning(
                        'Missing permission: %s',
                        required_permission_names)
                    raise Forbidden('Missing permission')


AnyCallable = Callable[[Any], Any]


def permission_required(
        required_permission_names: list[str],
) -> Callable[[AnyCallable], AnyCallable]:
    """
    Decorator to enforce required permissions for a function.
    
    This decorator ensures that the user associated with the provided
    `_user_uuid` in `kwargs` has the necessary permissions to access the
    decorated function. It interacts with a `PermissionChecker` object to
    determine if the required permissions are satisfied.
    
    Parameters:
        required_permission_names (list[str]): A list of permission names that are
            required to execute the decorated function.
    Raises:
        KeyError: If `_user_uuid` or `_permission_checker` is missing in the
            `kwargs` of the decorated function.
        Forbidden: If the user does not have the required permissions.
    """

    def check_permission(original_func: AnyCallable) -> AnyCallable:
        @functools.wraps(original_func)
        async def wrapper(*args, **kwargs):
            try:
                user_uuid = kwargs['_user_uuid']
                permission_checker = kwargs['_permission_checker']
            except KeyError as err:
                logger.error(
                    'Missing `_user_uuid` or `_permission_checker` '
                    'in kwargs: %s', err)
                raise err

            await permission_checker.permitted(
                user_uuid,
                required_permission_names,
            )
            return await original_func(*args, **kwargs)

        return wrapper

    return check_permission
