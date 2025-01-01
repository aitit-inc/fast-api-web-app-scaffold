"""Base class of application use cases."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

T = TypeVar('T')


class BaseUseCase(ABC, Generic[T]):
    """
    Base class for all application use cases.

    This class should be inherited by all use case classes
    to enforce a common structure and behavior.
    """

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """
        Execute the use case. Subclasses must implement this method.
        """


class AsyncBaseUseCase(ABC, Generic[T]):
    """
    Async base class for all application use cases.

    This class should be inherited by asynchronous use case classes
    to enforce a common structure and behavior.
    """

    @abstractmethod
    async def __call__(self, *args: Any, **kwargs: Any) -> T:
        """
        Execute the async use case. Subclasses must implement this method.
        """
