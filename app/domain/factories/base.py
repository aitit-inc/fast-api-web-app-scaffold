"""
This module defines a generic factory base class for creating domain entities.

The BaseEntityFactory abstract class serves as a foundation for implementing
factories that generate specific types of domain entities. Subclasses of this
base class must implement the `create` method to define entity-specific
creation logic.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

T = TypeVar('T', covariant=True)


class BaseEntityFactory(Generic[T], ABC):
    """
    Base factory class for creating domain entities.
    """

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """
        Abstract method to create an instance of a domain entity.
    
        Subclasses must implement this method to define the creation logic.
        This method will be used to instantiate and return a specific
        type of domain entity.
    
        Parameters:
            *args (Any): Positional arguments required for entity creation.
            **kwargs (Any): Keyword arguments required for entity creation.
    
        Returns:
            T: An instance of the domain entity.
        """
