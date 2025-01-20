"""Auth objects factories"""
from datetime import datetime, timedelta
from typing import Any, Callable

from app.domain.factories.base import BaseEntityFactory
from app.domain.services.token_auth import JwtPayload
from app.domain.services.time import to_utc


class JwtPayloadFactory(
    BaseEntityFactory[JwtPayload],
):
    """Create a new jwt token"""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
            self,
            issuer: str,
            audience: str,
            access_token_expire_minutes: int,
            refresh_token_expire_minutes: int,
            get_now: Callable[[], datetime],
    ) -> None:
        """Initialize."""
        self._iss = issuer
        self._aud = audience
        self._access_token_expire_minutes = access_token_expire_minutes
        self._refresh_token_expire_minutes = refresh_token_expire_minutes
        self._get_now = get_now

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __call__(
            self,
            sub: str,
            email: str,
            *args: Any,
            aud: str | None = None,
            nbf: datetime | None = None,
            jti: str | None = None,
            is_refresh_token: bool = False,
            **kwargs: Any,
    ) -> JwtPayload:
        """Create a new jwt token"""
        expire_minutes = self._refresh_token_expire_minutes \
            if is_refresh_token else self._access_token_expire_minutes

        now = to_utc(self._get_now())
        expires_delta = timedelta(minutes=expire_minutes)
        expire_dt = now + expires_delta

        nbf_dt = now if nbf is None else to_utc(nbf)

        return JwtPayload(
            iss=self._iss,
            sub=sub,
            aud=aud or self._aud,
            exp=int(expire_dt.timestamp()),
            email=email,
            nbf=int(nbf_dt.timestamp()),
            iat=int(now.timestamp()),
            jti=jti,
            is_refresh_token=is_refresh_token,
        )
