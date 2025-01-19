"""Handlers for the application."""
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.domain.exc import CustomBaseException
from app.interfaces.views.json_response import ErrorJsonResponseDetail, \
    error_json_response

logger = logging.getLogger('uvicorn')


def return_error_json_response(
        exc: Exception,
        status_code: int,
        detail: str | None
) -> JSONResponse:
    """Return an error response."""
    return JSONResponse(
        status_code=status_code,
        content=error_json_response(
            detail=[ErrorJsonResponseDetail(
                type=exc.__class__.__name__,
                msg=f'{exc}',
                detail=detail,
            )])
    )


def app_error_handlers(app_: FastAPI) -> None:
    """Add handlers to the application."""

    @app_.exception_handler(CustomBaseException)
    async def custom_exception_handler(
            _request: Request,
            exc: CustomBaseException) -> JSONResponse:
        logger.error('%s', exc)
        return return_error_json_response(
            exc, exc.status_code, exc.detail)

    @app_.exception_handler(HTTPException)
    async def http_exception_handler(
            _request: Request,
            exc: HTTPException) -> JSONResponse:
        logger.error('%s', exc)
        return return_error_json_response(
            exc, exc.status_code, None)

    # Final fall back case
    @app_.exception_handler(Exception)
    async def generic_error_handler(
            _request: Request,
            exc: Exception) -> JSONResponse:
        logger.exception(
            '%s, %s',
            exc.__class__.__name__, exc,
            exc_info=exc,
        )
        return return_error_json_response(
            exc, 500, None)
