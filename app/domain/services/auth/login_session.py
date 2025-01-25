"""Session auth service.
"""
from abc import ABC, abstractmethod

from app.domain.entities.login_session import LoginSession


class LoginSessionService(ABC):
    """Login Session service."""

    @abstractmethod
    def create_session(self, user_identifier: str) -> LoginSession:
        """Create a new session."""
