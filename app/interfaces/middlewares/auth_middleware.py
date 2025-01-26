"""Authorization Middlewares."""
import fnmatch
from logging import getLogger
from typing import Callable, Awaitable, cast

from fastapi import Request, Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.application.exc import Unauthorized
from app.domain.entities.login_session import LoginSession
from app.domain.services.auth.token import JwtPayload
from app.interfaces.controllers.path import API_BASE_PATH, API_V1_PATH, \
    HEALTH_CHECK_ENDPOINT
from app.interfaces.controllers.v1.path import AUTH_TOKEN_PREFIX, \
    REFRESH_ENDPOINT, SAMPLE_ITEMS_PREFIX, SAMPLE_ITEMS_BY_UUID_PREFIX, \
    EXPLICIT_TOKEN_ME_ENDPOINT, AUTH_SESSION_PREFIX, SESSION_LOGIN_ENDPOINT
from app.interfaces.middlewares.authorizer import AccessTokenAuthorizer, \
    SessionCookieAuthorizer, AuthMethod
from app.interfaces.middlewares.error_handlers import \
    return_error_json_response

logger = getLogger('uvicorn')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class AuthorizationMiddleware(BaseHTTPMiddleware):
    """Authorization Middleware."""
    _verification_excluded_paths: list[str] = [
        # API documentation
        '/docs', '/redoc', '/openapi.json',

        # session auth login
        f'{API_V1_PATH}{AUTH_SESSION_PREFIX}{SESSION_LOGIN_ENDPOINT}',

        # token auth login, refresh, custom
        f'{API_V1_PATH}{AUTH_TOKEN_PREFIX}',
        f'{API_V1_PATH}{AUTH_TOKEN_PREFIX}{REFRESH_ENDPOINT}',
        f'{API_V1_PATH}{AUTH_TOKEN_PREFIX}{EXPLICIT_TOKEN_ME_ENDPOINT}',

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
                 access_token_authorizer: AccessTokenAuthorizer,
                 session_cookie_authorizer: SessionCookieAuthorizer,
                 auth_method: AuthMethod,
                 ):
        super().__init__(app)
        self._access_token_authorizer = access_token_authorizer
        self._session_cookie_authorizer = session_cookie_authorizer
        self._auth_method_value = auth_method

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

        try:
            if self._auth_method == AuthMethod.SESSION_COOKIE:
                request = await self._session_cookie_authorizer.authorize(
                    request)
            elif self._auth_method == AuthMethod.BEARER_ACCESS_TOKEN:
                request = await self._access_token_authorizer.authorize(
                    request)
            else:
                logger.warning('Invalid auth method: %s', self._auth_method)
                raise Unauthorized('Unauthorized.')

            return await call_next(request)
        except Unauthorized as exc:
            return return_error_json_response(
                exc, exc.status_code, exc.detail)

    def is_excluded_path(self, path: str) -> bool:
        """excluded path check"""
        path = path.rstrip('/')
        for pattern in self._verification_excluded_paths:
            if fnmatch.fnmatch(path, pattern):
                return True

        return False

    @property
    def _auth_method(self) -> AuthMethod:
        return self._auth_method_value


def get_user_id(request: Request) -> int:
    """Get user id."""
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401, detail='Unauthorized')

    return cast(int, request.state.user_id)


def get_user_uuid(request: Request) -> str:
    """Get user uuid."""
    if not hasattr(request.state, 'user_uuid'):
        raise HTTPException(status_code=401, detail='Unauthorized')

    return cast(str, request.state.user_uuid)


def get_token_payload(request: Request) -> JwtPayload:
    """Get token payload."""
    if not hasattr(request.state, 'payload'):
        raise HTTPException(status_code=401, detail='Unauthorized')

    return cast(JwtPayload, request.state.payload)


def get_session(request: Request) -> LoginSession:
    """Get session payload."""
    if not hasattr(request.state, 'session'):
        raise HTTPException(status_code=401, detail='Unauthorized')

    return cast(LoginSession, request.state.session)
