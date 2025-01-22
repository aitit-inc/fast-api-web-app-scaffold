"""Session auth dtos."""
from enum import Enum

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Login request DTO."""
    username: str = Field(..., min_length=1, max_length=512)
    password: str = Field(..., min_length=1, max_length=512)


class SameSite(str, Enum):
    """Same site enum."""
    LAX = 'lax'
    STRICT = 'strict'
    NONE = 'none'


class SessionCookieConfig(BaseModel):
    """Session cookie config DTO."""
    key: str
    httponly: bool
    max_age: int
    samesite: SameSite
    secure: bool


class SessionCookie(SessionCookieConfig):
    """Session cookie DTO."""
    value: str
