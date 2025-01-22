"""Auth dtos."""
from datetime import datetime

from app.domain.services.auth.token import JwtPayload


class JwtPayloadRead(JwtPayload):
    """JWT payload read model"""
    exp_dt: datetime | None = None
    nbf_dt: datetime | None = None
    iat_dt: datetime | None = None
