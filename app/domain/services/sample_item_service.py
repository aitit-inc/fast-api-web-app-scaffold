"""SampleItem service."""
from app.domain.entities.sample_item import SampleItem, SampleItemLengths


# pylint: disable=too-few-public-methods
class SampleItemService:
    """Service class for processing SampleItem."""

    @staticmethod
    def calculate_lengths(sample_item: SampleItem) -> SampleItemLengths:
        """
        Calculate the lengths of `name` and `description` fields of a
        SampleItem instance.

        Args:
            sample_item (SampleItem): An instance of SampleItem.

        Returns:
            SampleItemLengths: An object containing the lengths of the `name`
            and `description` fields.
        """
        return SampleItemLengths(
            name_length=len(sample_item.name),
            description_length=len(sample_item.description),
        )
