"""SampleItem list use case."""
from typing import Coroutine, Any, Awaitable
from fastapi_pagination import Page

from app.application.use_cases.base import AsyncBaseUseCase
from app.domain.entities.sample_item import SampleItem
from app.domain.repositories.sample_item import SampleItemRepository


class SampleItemListUseCase(AsyncBaseUseCase[Page[SampleItem]]):
    """SampleItem list use case."""

    def __init__(self, repository: SampleItemRepository) -> None:
        """Constructor."""
        self._repository = repository

    async def __call__(
            self,
            *args: object,
            **kwargs: object
    ) -> Page[SampleItem]:
        """Execute the use case."""
        return await self._repository.get_list()
