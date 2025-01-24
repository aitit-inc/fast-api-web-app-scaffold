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
            session_id: str,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        await self._login_session_repository.delete(session_id)
