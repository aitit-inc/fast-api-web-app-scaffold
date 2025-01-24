"""LoginSession service implement."""
from datetime import datetime, timedelta
from typing import Callable

from itsdangerous import URLSafeSerializer
from shortuuid import uuid

from app.domain.entities.login_session import LoginSession, SessionData
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
            uuid_gen: Callable[[], str] = uuid,
    ) -> None:
        """Initialize."""
        self._login_session_secret_key = login_session_secret_key
        self._login_session_expire_minutes = login_session_expire_minutes
        self._get_now = get_now
        self._uuid_gen = uuid_gen

    def create_session(self, user_identifier: str) -> LoginSession:
        serializer = URLSafeSerializer(self._login_session_secret_key)
        session_unique_str = self._gen_uuid()
        session_data = SessionData(
            user_id=user_identifier,
            session_unique_str=session_unique_str,
        )
        session_id = serializer.dumps(session_data.model_dump())

        now = to_utc(self._get_now())
        expires_delta = timedelta(minutes=self._login_session_expire_minutes)
        expires_at = now + expires_delta

        return LoginSession(
            id=session_id,
            user_id=user_identifier,
            session_unique_str=session_unique_str,
            expires_at=expires_at,
        )

    def decode_session(self, session_id: str) -> SessionData:
        serializer = URLSafeSerializer(self._login_session_secret_key)
        session_data = serializer.loads(session_id)
        return SessionData(**session_data)

    def _gen_uuid(self) -> str:
        return self._uuid_gen()
