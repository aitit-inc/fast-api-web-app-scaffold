"""Exception classes.

Exception classes should be defined at appropriate layers,
such as the domain, application, infrastructure, or interfaces,
to ensure proper separation of concerns and maintainability.
"""
from app.domain.exc import CustomBaseException


class InvalidCredentials(CustomBaseException):
    """Raised when invalid credentials are provided."""


class InvalidToken(CustomBaseException):
    """Raised when an invalid token is provided."""


class TokenExpired(CustomBaseException):
    """Raised when a token is expired."""


class Unauthorized(CustomBaseException):
    """Raised when a user is not authorized to perform an action."""


class EntityAlreadyExists(CustomBaseException):
    """Raised when a user already exists."""


class EntityNotFound(CustomBaseException):
    """Raised when a user is not found."""

    @staticmethod
    def to_msg(entity_id: int | str) -> str:
        return f'Entity with id {entity_id} not found.'


class UniqueConstraintViolation(CustomBaseException):
    """Raised when a unique constraint is violated."""


class OperationNotAllowed(CustomBaseException):
    """Raised when an operation is not allowed."""
