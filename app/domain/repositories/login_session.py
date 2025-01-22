"""LoginSession repository interface."""
from abc import ABC

from app.domain.entities.login_session import LoginSession
from app.domain.repositories.base import AsyncBaseRepository


class LoginSessionRepository(
    AsyncBaseRepository[str, LoginSession],
    ABC
):
    """LoginSession repository interface."""
