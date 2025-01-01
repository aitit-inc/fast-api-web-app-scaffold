"""Exception classes.

Exception classes should be defined at appropriate layers,
such as the domain, application, infrastructure, or interfaces,
to ensure proper separation of concerns and maintainability.
"""


class CustomBaseException(Exception):
    """Base exception for all custom exceptions."""

    def __init__(self, message: str, detail: str | None = None):
        self.message = message
        self.detail = detail

    def __str__(self) -> str:
        class_name = self.__class__.__name__

        def construct_message() -> str:
            return f'{class_name}: {self.message}'

        return construct_message()
