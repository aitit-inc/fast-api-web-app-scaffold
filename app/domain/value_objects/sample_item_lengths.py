"""SampleItem lengths"""
from pydantic import BaseModel


class SampleItemLengths(BaseModel):
    """Value object to represent lengths of SampleItem fields."""
    name_length: int
    description_length: int
