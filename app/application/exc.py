"""Exception classes.

Exception classes should be defined at appropriate layers,
such as the domain, application, infrastructure, or interfaces,
to ensure proper separation of concerns and maintainability.
"""
from app.domain.exc import CustomBaseException


class InvalidCredentials(CustomBaseException):
    """Raised when invalid credentials are provided."""
    _status_code = 401


class InvalidToken(CustomBaseException):
    """Raised when an invalid token is provided."""
    _status_code = 401


class TokenExpired(CustomBaseException):
    """Raised when a token is expired."""
    _status_code = 401


class Unauthorized(CustomBaseException):
    """Raised when a user is not authorized to perform an action."""
    _status_code = 403


class EntityAlreadyExists(CustomBaseException):
    """Raised when a user already exists."""
    _status_code = 409


class EntityNotFound(CustomBaseException):
    """Raised when a user is not found."""
    _status_code = 404

    @staticmethod
    def to_msg(entity_id: int | str) -> str:
        """Convert entity ID to a not found message."""
        return f"Entity with ID '{entity_id}' was not found."


class UniqueConstraintViolation(CustomBaseException):
    """Raised when a unique constraint is violated."""
    _status_code = 409


class OperationNotAllowed(CustomBaseException):
    """Raised when an operation is not allowed."""
    _status_code = 403
