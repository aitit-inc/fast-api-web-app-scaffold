"""Session auth service.
"""
from abc import ABC, abstractmethod

from app.domain.entities.login_session import LoginSession


# TODO: Change to LoginSessionFactory instead of a service
class LoginSessionService(ABC):
    """Login Session service."""

    @abstractmethod
    async def create_session(self, user_identifier: str) -> LoginSession:
        """Create a new session."""
