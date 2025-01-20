"""Common functions for auth use cases."""
from datetime import datetime, timezone

from app.domain.services.token_auth import JwtPayload
from app.application.dto.token_auth import JwtPayloadRead


def jwt_payload_to_read(payload: JwtPayload) -> JwtPayloadRead:
    """Transform a JWT payload to a read model."""
    read_model = JwtPayloadRead.model_validate(payload.model_dump())

    read_model.exp_dt = datetime.fromtimestamp(
        payload.exp, tz=timezone.utc
    )
    read_model.nbf_dt = datetime.fromtimestamp(
        payload.nbf, tz=timezone.utc
    )
    read_model.iat_dt = datetime.fromtimestamp(
        payload.iat, tz=timezone.utc
    )

    return read_model
