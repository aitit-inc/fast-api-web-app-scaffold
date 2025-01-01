"""SampleItem repository in memory."""

from app.domain.entities.sample_item import SampleItem
from app.domain.factories.sample_item import SampleItemFactory
from app.domain.repositories.base import FiltersType
from app.domain.repositories.sample_item import SampleItemRepository


class InMemorySampleItemRepository(SampleItemRepository):
    """In-memory repository implementation for SampleItem."""

    def __init__(self, factory: SampleItemFactory, ) -> None:
        self._items: list[SampleItem] = [
            factory('foo', 'foo description', id_=1),
            factory('bar baz', 'bar baz description', id_=2, ),
        ]

    def get_by_id(self, entity_id: int) -> SampleItem | None:
        """Retrieve the entity with the specified ID."""
        for item in self._items:
            if item.id == entity_id:
                return item
        return None

    def get_list(self, filters: FiltersType = None) -> list[SampleItem]:
        """Retrieve a list of entities (with optional filtering)."""
        if not filters:
            return self._items
        filtered_items = self._items
        for key, value in filters.items():
            filtered_items = [item for item in filtered_items if
                              getattr(item, key) == value]
        return filtered_items

    def add(self, entity: SampleItem) -> SampleItem:
        """Add an entity."""
        if not entity.id:
            raise ValueError("Entity ID is required.")

        if self.get_by_id(entity.id):
            raise ValueError(f"Entity with ID {entity.id} already exists.")

        self._items.append(entity)
        return entity

    def update(self, entity: SampleItem) -> SampleItem:
        """Update an entity."""
        if not entity.id:
            raise ValueError("Entity ID is required.")

        existing_entity = self.get_by_id(entity.id)
        if not existing_entity:
            raise ValueError(f"Entity with ID {entity.id} does not exist.")
        self._items = [item if item.id != entity.id else entity for item in
                       self._items]
        return entity

    def delete(self, entity_id: int) -> None:
        """Delete the entity with the specified ID."""
        self._items = [item for item in self._items if item.id != entity_id]
