"""User authentication and authorization services"""
from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel


class TokenType(str, Enum):
    """Token type enum"""
    BEARER = 'bearer'


class Token(BaseModel):
    """Token model"""
    access_token: str
    refresh_token: str | None = None
    token_type: TokenType


class JwtPayload(BaseModel):
    """JWT payload model"""
    iss: str
    sub: str
    aud: str
    exp: int
    nbf: int
    iat: int
    jti: str | None = None
    email: str
    is_refresh_token: bool


class JwtTokenService(ABC):
    """JWT token services"""

    @abstractmethod
    def create_token(self, data: JwtPayload) -> str:
        """Create access token"""

    @abstractmethod
    def verify_token(self, token: str) -> JwtPayload:
        """Authorize user"""
