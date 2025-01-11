"""Base API query value object"""
from enum import Enum
from logging import getLogger
from typing import Any

from pydantic import BaseModel

logger = getLogger('uvicorn')


class ApiListQueryOp(str, Enum):
    """Enum for API list query operators"""
    EQ = 'eq'
    NEQ = 'neq'
    LIKE = 'like'
    LT = 'lt'
    GT = 'gt'
    LTE = 'lte'
    GTE = 'gte'
    IN = 'in'
    NOTIN = 'notin'
    ASC = 'asc'
    DESC = 'desc'

    @staticmethod
    def list_values() -> list[str]:
        """Return list of values for the enum"""
        return [op.value for op in ApiListQueryOp]


class ApiListQuery(BaseModel):
    """Base API list query DTO"""
    queries: dict[str, Any]
