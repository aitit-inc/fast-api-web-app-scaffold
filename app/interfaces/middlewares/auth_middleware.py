"""Authentication/Authorization Middlewares."""
import fnmatch
from logging import getLogger
from typing import Callable, Awaitable, cast

from fastapi import Request, Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.application.exc import Unauthorized
from app.domain.services.auth import JwtTokenService, JwtPayload
from app.interfaces.controllers.path import API_BASE_PATH, API_V1_PATH, \
    HEALTH_CHECK_ENDPOINT
from app.interfaces.controllers.v1.path import AUTH_PREFIX, TOKEN_ENDPOINT, \
    REFRESH_ENDPOINT, SAMPLE_ITEMS_PREFIX, SAMPLE_ITEMS_BY_UUID_PREFIX, \
    EXPLICIT_TOKEN_ME_ENDPOINT
from app.interfaces.middlewares.error_handlers import \
    return_error_json_response

logger = getLogger('uvicorn')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class AccessTokenAuthorizationMiddleware(BaseHTTPMiddleware):
    """Access Token Authorization Middleware."""
    _verification_excluded_paths: list[str] = [
        # API documentation
        '/docs', '/redoc', '/openapi.json',

        # Auth
        f'{API_V1_PATH}{AUTH_PREFIX}{TOKEN_ENDPOINT}',
        f'{API_V1_PATH}{AUTH_PREFIX}{REFRESH_ENDPOINT}',
        f'{API_BASE_PATH}{AUTH_PREFIX}{EXPLICIT_TOKEN_ME_ENDPOINT}',

        # Admin console
        # '/admin', '/admin/', '/admin/*',

        # For health check
        f'{API_BASE_PATH}{HEALTH_CHECK_ENDPOINT}',

        # Add paths to exclude from verification
        f'{API_V1_PATH}{SAMPLE_ITEMS_PREFIX}',
        f'{API_V1_PATH}{SAMPLE_ITEMS_PREFIX}/*',
        f'{API_V1_PATH}{SAMPLE_ITEMS_BY_UUID_PREFIX}',
        f'{API_V1_PATH}{SAMPLE_ITEMS_BY_UUID_PREFIX}/*',
        # '/some/public/paths/*',
    ]

    def __init__(self,
                 app: ASGIApp,
                 jwt_token_service: JwtTokenService,
                 ):
        super().__init__(app)
        self._jwt_token_service = jwt_token_service

    async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Dispatch"""
        # Check if the path is excluded
        if self.is_excluded_path(request.url.path):
            # Skip verification for public paths
            return await call_next(request)

        # Extract token from Authorization header
        try:
            token = await oauth2_scheme(request)
        except HTTPException as _err:
            logger.warning('HTTPException: %s', _err)
            token = None

        if token is None:
            logger.warning(
                'Failed to extract token from Authorization header.')
            exc = Unauthorized('Invalid or missing token.')

            return return_error_json_response(
                exc, exc.status_code, exc.detail)

        payload = self._jwt_token_service.verify_token(token)

        request.state.user_id = payload.sub
        request.state.payload = payload

        return await call_next(request)

    def is_excluded_path(self, path: str) -> bool:
        """excluded path check"""
        path = path.rstrip('/')
        for pattern in self._verification_excluded_paths:
            if fnmatch.fnmatch(path, pattern):
                return True

        return False


def get_token_payload(request: Request) -> JwtPayload:
    """Get token payload."""
    if not hasattr(request.state, 'payload'):
        raise HTTPException(status_code=401, detail='Unauthorized')

    return cast(JwtPayload, request.state.payload)
