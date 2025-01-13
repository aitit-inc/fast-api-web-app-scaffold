"""Serializer base models."""
from logging import getLogger
from typing import Type, Any

from pydantic import BaseModel, ConfigDict, model_validator
from sqlmodel import SQLModel
from sqlmodel.main import FieldInfo

from app.domain.value_objects.api_query import ApiListQueryOp, \
    ApiListQuery

logger = getLogger('uvicorn')


class ApiListQueryDtoBaseModel(BaseModel):
    """BaseModel for validating the naming conventions of field names"""

    __entity_cls__: Type[SQLModel] | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def get_entity_fields(cls) -> dict[str, FieldInfo] | None:
        """Get the set of fields from the __entity_cls__ SQLModel"""
        if not cls.__entity_cls__:
            logger.warning('__entity_cls__ is not set in %s', cls)
            return None

        return cls.__entity_cls__.model_fields  # type: ignore

    @model_validator(mode='before')
    @classmethod
    def validate_field_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate field names to follow the '{name}__{op}' format"""
        allowed_ops = set(ApiListQueryOp.list_values())
        entity_fields = cls.get_entity_fields()

        for field_name in values.keys():
            if '__' in field_name:
                # Split the field name into 'name' and 'op'
                parts = field_name.split('__')
                if len(parts) != 2:
                    raise ValueError(
                        f"The field name '{field_name}' must follow the "
                        f"'{{name}}__{{op}}' format."
                    )
                name, op = parts
                if entity_fields:
                    if name not in entity_fields:
                        raise ValueError(
                            f"'{name}' is not a valid field in the "
                            f"entity class."
                        )
                    # TODO: Perform type checking of query fields against
                    #  entity fields.

                if op not in allowed_ops:
                    raise ValueError(
                        f"The operator '{op}' in field name '{field_name}' "
                        f"is not allowed."
                    )
            else:
                raise ValueError(
                    f"The field name '{field_name}' must contain '__'."
                )
        return values

    def to_domain(self) -> ApiListQuery:
        """Convert to domain object."""
        return ApiListQuery(
            queries=self.model_dump(exclude_none=True),
        )
