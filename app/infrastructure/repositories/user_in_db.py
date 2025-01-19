"""User repository in DB"""
from datetime import datetime
from logging import getLogger
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.user import UserRepository, \
    UserByUUIDRepository, UserByEmailRepository, UserQueryFactory
from app.infrastructure.repositories.base import InDBBaseEntityRepository, \
    InDBBaseQueryFactory

logger = getLogger('uvicorn')


class InDBUserRepository(
    UserRepository,
    InDBBaseEntityRepository[int, User],
):
    """In-DB User repository."""
    _entity_cls = User

    @staticmethod
    def factory(
            get_now: Callable[[], datetime]
    ) -> Callable[[AsyncSession], 'InDBUserRepository']:
        """Factory method."""
        return lambda db_session: InDBUserRepository(db_session, get_now)


class InDBUserByEmailRepository(
    UserByEmailRepository,
    InDBBaseEntityRepository[str, User],
):
    """In-DB User repository by email."""
    _entity_cls = User
    _id_field = 'email'

    @staticmethod
    def factory(
            get_now: Callable[[], datetime]
    ) -> Callable[[AsyncSession], 'InDBUserByEmailRepository']:
        """Factory method."""
        return lambda db_session: InDBUserByEmailRepository(
            db_session, get_now)


class InDBUserByUUIDRepository(
    UserByUUIDRepository,
    InDBBaseEntityRepository[str, User],
):
    """In-DB User repository by UUID."""
    _entity_cls = User
    _id_field = 'uuid'

    @staticmethod
    def factory(
            get_now: Callable[[], datetime]
    ) -> Callable[[AsyncSession], 'InDBUserByUUIDRepository']:
        """Factory method."""
        return lambda db_session: InDBUserByUUIDRepository(db_session, get_now)


class InDBUserQueryFactory(
    UserQueryFactory,
    InDBBaseQueryFactory[User]
):
    """In-DB User query."""
    _entity_cls = User
