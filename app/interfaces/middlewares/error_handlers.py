"""Handlers for the application."""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exc import CustomBaseException
from app.interfaces.views.json_response import ErrorJsonResponseDetail, \
    error_json_response

logger = logging.getLogger('uvicorn')


def app_error_handlers(app_: FastAPI) -> None:
    """Add handlers to the application."""

    @app_.exception_handler(CustomBaseException)
    async def custom_exception_handler(
            _request: Request,
            exc: CustomBaseException) -> JSONResponse:
        logger.error('%s', exc)
        return JSONResponse(
            status_code=exc.status_code,
            content=error_json_response(
                detail=[ErrorJsonResponseDetail(
                    type=exc.__class__.__name__,
                    msg=f'{exc}',
                    detail=exc.detail,
                )])
        )

    # Final fall back case
    @app_.exception_handler(Exception)
    async def generic_error_handler(_request: Request,
                                    exc: Exception) -> JSONResponse:
        logger.error('%s', exc)
        return JSONResponse(
            status_code=500,
            content=error_json_response(
                detail=[ErrorJsonResponseDetail(
                    type=exc.__class__.__name__,
                    msg=f'An unexpected error occurred. {exc}',
                    detail=None,
                )])
        )
