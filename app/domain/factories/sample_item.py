"""SampleItem factory."""
from datetime import datetime
from typing import Callable

from app.domain.entities.sample_item import SampleItem
from app.domain.factories.base import BaseEntityFactory


class SampleItemFactory(BaseEntityFactory[SampleItem]):
    """SampleItem factory."""

    def __init__(self, get_now: Callable[[], datetime]):
        super().__init__()
        self._get_now = get_now

    def __call__(
            self,
            name: str,
            description: str,
            id_: int | None = None,
    ) -> SampleItem:
        """Create a SampleItem instance."""
        return SampleItem(
            id=id_,
            name=name,
            description=description,
            created_at=self._get_now(),
        )
