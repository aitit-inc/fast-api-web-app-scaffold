"""SampleItem mapper."""
from shortuuid import uuid

from app.domain.entities.sample_item import SampleItemCreate, SampleItem


def sample_item_from_create(data: SampleItemCreate) -> SampleItem:
    """Create SampleItem from SampleItemCreate."""
    data_dict = data.model_dump()
    data_dict['uuid'] = uuid()
    return SampleItem.model_validate(data_dict)
