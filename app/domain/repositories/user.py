"""User repository interface."""
from abc import ABC

from app.domain.entities.user import User, UserCreate, UserUpdate
from app.domain.repositories.base import AsyncBaseRepository


class UserRepository(
    AsyncBaseRepository[int, User, UserCreate, UserUpdate],
    ABC
):
    """User repository interface."""
