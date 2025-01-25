"""LoginSession service implement."""
import secrets
from datetime import datetime, timedelta
from typing import Callable

from app.domain.entities.login_session import LoginSession
from app.domain.services.auth.login_session import LoginSessionService
from app.domain.services.time import to_utc


class LoginSessionServiceImpl(
    LoginSessionService,
):
    """LoginSession service implement."""

    def __init__(
            self,
            login_session_secret_key: str,
            login_session_expire_minutes: int,
            get_now: Callable[[], datetime],
    ) -> None:
        """Initialize."""
        self._login_session_secret_key = login_session_secret_key
        self._login_session_expire_minutes = login_session_expire_minutes
        self._get_now = get_now

    def create_session(self, user_identifier: str) -> LoginSession:
        session_id = self._generate_session_id()

        now = to_utc(self._get_now())
        expires_delta = timedelta(minutes=self._login_session_expire_minutes)
        expires_at = now + expires_delta

        return LoginSession(
            id=session_id,
            user_id=user_identifier,
            expires_at=expires_at,
        )

    @staticmethod
    def _generate_session_id() -> str:
        """
        Generates a cryptographically secure random session ID
        as a 256-bit (32-byte) URL-safe Base64 string.
        """
        return secrets.token_urlsafe(32)
