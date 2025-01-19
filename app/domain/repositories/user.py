"""User repository interface."""
from abc import ABC

from app.domain.entities.user import User
from app.domain.repositories.base import AsyncBaseRepository, BaseQueryFactory


class UserRepository(
    AsyncBaseRepository[int, User],
    ABC
):
    """User repository interface."""


class UserQueryFactory(
    BaseQueryFactory[User],
    ABC
):
    """User query."""


class UserByEmailRepository(
    AsyncBaseRepository[str, User],
    ABC
):
    """User by Email repository interface."""


class UserByUUIDRepository(
    AsyncBaseRepository[str, User],
    ABC
):
    """User by UUID repository interface."""
