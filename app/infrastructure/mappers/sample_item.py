"""SampleItem mapper."""
from app.domain.entities.sample_item import SampleItemCreate, SampleItem, \
    SampleItemRead


def sample_item_from_create(data: SampleItemCreate) -> SampleItem:
    """Create SampleItem from SampleItemCreate."""
    return SampleItem.model_validate(data)


def sample_item_to_read(data: SampleItem) -> SampleItemRead:
    """Read SampleItem from SampleItem."""
    return SampleItemRead.model_validate(data)