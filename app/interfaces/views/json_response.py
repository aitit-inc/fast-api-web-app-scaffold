"""
This file defines an application-wide JSON response format. 
The purpose is to ensure all responses in the application follow a consistent
structure for better maintainability and user understanding.
"""
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class ErrorJsonResponseDetail(BaseModel):
    """JSON response format for error responses."""
    type: str
    msg: str
    detail: str | None = None


class ErrorJsonResponse(BaseModel):
    """JSON response format for error responses."""
    detail: list[ErrorJsonResponseDetail]


def error_json_response(
        detail: list[ErrorJsonResponseDetail]) -> Any:
    """Helper function to create an error JSON response."""
    return jsonable_encoder(ErrorJsonResponse(detail=detail))
