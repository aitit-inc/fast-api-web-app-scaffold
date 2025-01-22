"""Base auth services."""
from abc import ABC, abstractmethod

from app.domain.entities.user import User


class UserAuthService(ABC):
    """User authentication and authorization services"""

    @abstractmethod
    async def authenticate(self, username: str, password: str) -> User | None:
        """Authenticate user"""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash password"""
