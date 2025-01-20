"""Application module."""
import logging
from contextlib import asynccontextmanager
from logging import getLogger
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.di_container import Container
from app.infrastructure.config.config import get_settings
from app.interfaces.controllers.base import router
from app.interfaces.middlewares.token_auth_middleware import \
    AccessTokenAuthorizationMiddleware
from app.interfaces.middlewares.error_handlers import app_error_handlers

logger = getLogger('uvicorn')


def create_app() -> FastAPI:
    """Create FastAPI application."""
    container = Container()
    config = get_settings()

    _db = container.db()

    # basicConfig() is always required for sqlalchemy
    logging.basicConfig(level=config.log_level)
    logging.getLogger('uvicorn').setLevel(config.log_level)

    @asynccontextmanager
    async def lifespan(_app: FastAPI):  # type: ignore
        # do something before start
        yield
        # do something before end

    _app = FastAPI(
        lifespan=lifespan,
        swagger_ui_parameters={
            # Can expand all sections by default by uncommenting the line below
            # 'docExpansion': 'full',
            # 'defaultModelsExpandDepth': 100,
            # 'defaultModelExpandDepth': 100,
        },
    )
    _app.container = container  # type: ignore
    _app.include_router(router)

    app_error_handlers(_app)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=config.origins,

        # TODO: set in config
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    _app.add_middleware(
        AccessTokenAuthorizationMiddleware,
        jwt_token_service=container.jwt_token_service(),
    )

    # _app.mount('/admin', admin_app)

    def custom_openapi() -> dict[str, Any]:
        if _app.openapi_schema:
            return _app.openapi_schema

        openapi_schema: dict[str, Any] = get_openapi(
            title=f"{config.app_name} API",
            version='0.0.1',
            description=f"{config.app_name} API",
            routes=app.routes,
        )
        # openapi_schema["components"]["securitySchemes"] = {
        #     "BearerAuth": {
        #         "type": "http",
        #         "scheme": "bearer",
        #         "bearerFormat": "JWT",
        #     }
        # }
        # openapi_schema["security"] = [{"BearerAuth": []}]
        _app.openapi_schema = openapi_schema
        return _app.openapi_schema

    _app.openapi = custom_openapi  # type: ignore

    logger.info('Application created')
    return _app


app = create_app()
