"""SampleItem mapper."""
from shortuuid import uuid

from app.domain.entities.sample_item import SampleItemCreate, SampleItem, \
    SampleItemRead, SampleItemReadWithMeta
from app.domain.services.sample_item_service import SampleItemService


def sample_item_from_create(data: SampleItemCreate) -> SampleItem:
    """Create SampleItem from SampleItemCreate."""
    data_dict = data.model_dump()
    data_dict['uuid'] = uuid()
    return SampleItem.model_validate(data_dict)


def sample_item_to_read(data: SampleItem) -> SampleItemRead:
    """Read SampleItem from SampleItem."""
    return SampleItemRead.model_validate(data)


def sample_item_with_meta_to_read(data: SampleItem) -> SampleItemReadWithMeta:
    """Read SampleItem with meta from SampleItem."""
    lengths = SampleItemService.calculate_lengths(data)
    merged = data.model_dump() | {'meta_data': lengths.model_dump()}
    return SampleItemReadWithMeta.model_validate(merged)
