"""SampleItem entity."""

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from app.domain.entities.common import MAX_LEN_SHORT, \
    BaseSQLModel


class SampleItemBase(SQLModel):
    """SampleItem entity base class."""
    name: str = Field(
        max_length=MAX_LEN_SHORT, nullable=False,
        description='SampleItem name, description for pydantic and openapi',
        sa_column_kwargs={'comment': 'SampleItem name, comment for db'}
    )
    description: str | None = Field(
        nullable=True,
        description='SampleItem description for pydantic and openapi',
        sa_column_kwargs={'comment': 'SampleItem description for db'}
    )


class SampleItem(SampleItemBase, BaseSQLModel, table=True):
    """SampleItem entity."""
    __tablename__ = "sample_items"
    id: int | None = Field(default=None, primary_key=True, index=True)
    uuid: str = Field(
        unique=True, index=True, nullable=False,
        sa_column_kwargs={'comment': 'Short UUID generated by server'}
    )


class SampleItemLengths(BaseModel):
    """Value object to represent lengths of SampleItem fields."""
    name_length: int
    description_length: int
