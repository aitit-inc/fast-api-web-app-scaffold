"""Session auth service.
"""
from abc import ABC, abstractmethod

from app.domain.entities.login_session import LoginSession
from app.domain.entities.user import User


class LoginSessionService(ABC):
    """Login Session service."""

    @abstractmethod
    def create_session(self, user: User) -> LoginSession:
        """Create a new session."""
