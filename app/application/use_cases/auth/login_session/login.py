"""Login use case."""
from logging import getLogger
from typing import Any

from app.application.dto.session_auth import SessionCookie, SessionCookieConfig
from app.application.exc import InvalidCredentials
from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.repositories.login_session import LoginSessionRepository
from app.domain.services.auth.base import UserAuthService
from app.domain.services.auth.login_session import LoginSessionService

logger = getLogger('uvicorn')


class LoginUseCase(
    AsyncBaseUseCase[SessionCookie]
):
    """Login use case."""

    def __init__(
            self,
            user_auth_service: UserAuthService,
            login_session_service: LoginSessionService,
            login_session_repository: LoginSessionRepository,
    ):
        self._user_auth_service = user_auth_service
        self._login_session_service = login_session_service
        self._login_session_repository = login_session_repository

    async def __call__(
            self,
            username: str,
            password: str,
            session_cookie_config: SessionCookieConfig,
            *args: Any,
            **kwargs: Any,
    ) -> SessionCookie:
        user = await self._user_auth_service.authenticate(
            username, password)

        if user is None:
            logger.warning('Invalid email or password.')
            raise InvalidCredentials(
                'Invalid email or password.')

        session = await self._login_session_service.create_session(user.uuid)
        _added_session = await self._login_session_repository.add(session)

        cookie_data = session_cookie_config.model_dump() | {
            'value': session.id}

        return SessionCookie.model_validate(cookie_data)
