"""User repository interface."""
from abc import ABC

from app.domain.entities.user import User, UserUpdate
from app.domain.repositories.base import AsyncBaseRepository


class UserRepository(
    AsyncBaseRepository[int, User, UserUpdate],
    ABC
):
    """User repository interface."""
