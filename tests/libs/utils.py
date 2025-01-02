"""Utility functions for testing."""
from datetime import datetime
from typing import Any

from sqlalchemy import delete, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.domain.entities.sample_item import SampleItem
from app.infrastructure.config.config import Settings

API_BASE = '/api/v1'


def db_engine(config: Settings) -> Engine:
    """Create database engine."""
    sync_db_url = config.db_dsn.replace('+asyncpg', '')
    engine = create_engine(sync_db_url)
    return engine


def reset_id_seq(db_session: Session, seq: int | None = None) -> None:
    """Reset id sequence."""
    seq = 1 if not seq else seq
    id_seq_list = [
        'sample_items_id_seq',
    ]
    for id_seq in id_seq_list:
        statement = text(
            f'ALTER SEQUENCE {id_seq} RESTART WITH {seq};')
        db_session.execute(statement)


def reset_tables(db_session: Session) -> None:
    """Reset all tables."""
    entities = [SampleItem]
    for entity in entities:
        db_session.execute(delete(entity))

    reset_id_seq(db_session)


def mock_overwrite_datetime(
        data: dict[str, Any] | list[Any] | Any,
        dt: datetime,
        fields: list[str] | None = None,
) -> dict[str, Any] | list[Any] | Any:
    """
    Overwrite datetime fields in a dictionary or list
    of dictionaries with a specific datetime.

    Args:
        data (dict[str, Any] | list[Any] | Any):
            The input data, which can be a dictionary,
            a list of dictionaries, or any other data type.
        dt (datetime):
            The datetime object to overwrite the specified fields with.
        fields (list[str] | None):
            A list of field names to overwrite.
            Defaults to ["created_at", "updated_at"].

    Returns:
        dict[str, Any] | list[Any] | Any:
            The modified data with updated datetime fields,
            or the original input if the data type is unsupported.
    """
    fields = fields or ['created_at', 'updated_at']
    if not isinstance(data, dict):
        return data

    for key, value in data.items():
        if key in fields and value is not None:
            data[key] = dt.isoformat()
        if isinstance(value, dict):
            data[key] = mock_overwrite_datetime(value, dt)
        elif isinstance(value, list):
            data[key] = [mock_overwrite_datetime(item, dt) for item in value]
    return data
