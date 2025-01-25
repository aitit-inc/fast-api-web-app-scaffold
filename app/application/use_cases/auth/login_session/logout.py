"""Logout use case."""
from logging import getLogger
from typing import Any

from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.repositories.login_session import LoginSessionRepository

logger = getLogger('uvicorn')


class LogoutUseCase(
    AsyncBaseUseCase[None]
):
    """Logout use case."""

    def __init__(
            self,
            login_session_repository: LoginSessionRepository,
    ):
        self._login_session_repository = login_session_repository

    async def __call__(
            self,
            session_id: str | None,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        """Execute logout use case."""
        if session_id is None:
            logger.warning('Failed to extract session_id from cookies.')

            # During logout, even if the request is invalid and does not
            # contain a session, no error will be returned to the client.
            return

        await self._login_session_repository.delete(session_id)
