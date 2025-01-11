"""User repository interface."""
from abc import ABC

from app.domain.entities.user import User
from app.domain.repositories.base import AsyncBaseRepository


class UserRepository(
    AsyncBaseRepository[int, User],
    ABC
):
    """User repository interface."""
