"""Repository implementation base class."""
from abc import ABC
from typing import Generic

from sqlalchemy import select, Select

from app.domain.repositories.base import EntityT
from app.domain.value_objects.api_query import ApiListQuery, \
    ApiListQueryOp


class InDBQueryFactoryTrait(
    Generic[EntityT],
    ABC
):
    """Base query factory for in-database repositories."""

    @staticmethod
    def _list_query(
            api_query: ApiListQuery,
            model: type[EntityT],
    ) -> Select[tuple[EntityT]]:
        """Private method for constructing the list query."""
        stmt = select(model)
        queries = api_query.queries

        def _get_field_op(key_: str) -> tuple[str, str]:
            field_, op_ = key_.split('__')
            return field_, op_

        # operation mapping
        filter_operations = {
            ApiListQueryOp.EQ: lambda field_, value_: field_ == value_,
            ApiListQueryOp.NEQ: lambda field_, value_: field_ != value_,
            ApiListQueryOp.LIKE: lambda field_, value_: field_.ilike(value_),
            ApiListQueryOp.GT: lambda field_, value_: field_ > value_,
            ApiListQueryOp.GTE: lambda field_, value_: field_ >= value_,
            ApiListQueryOp.LT: lambda field_, value_: field_ < value_,
            ApiListQueryOp.LTE: lambda field_, value_: field_ <= value_,
            ApiListQueryOp.IN: lambda field_, value_: field_.in_(value_),
            ApiListQueryOp.NOTIN: lambda field_, value_: field_.notin_(value_),
        }

        for key, value in queries.items():
            # Filter query
            field, op = _get_field_op(key)
            field_obj = getattr(model, field)
            if op in filter_operations:
                stmt = stmt.where(
                    filter_operations[op](field_obj, value))  # type: ignore

        sort_operations = {
            ApiListQueryOp.ASC: lambda field_: field_,
            ApiListQueryOp.DESC: lambda field_: field_.desc(),
        }

        for key, value in queries.items():
            # Sort query
            field, op = _get_field_op(key)
            if op in sort_operations and value is True:
                stmt = stmt.order_by(
                    sort_operations[op](getattr(model, field)))  # type: ignore

        return stmt
