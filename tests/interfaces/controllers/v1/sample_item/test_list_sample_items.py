"""Test case for the list_sample_items endpoint of sample_items controller."""
import json
from datetime import datetime
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.infrastructure.config.config import get_settings_for_testing
from app.main import app
from tests.libs.mocks import add_sample_item
from tests.libs.utils import reset_tables, API_BASE, db_engine, \
    mock_overwrite_datetime


@pytest.fixture
def client(
        request: pytest.FixtureRequest) -> Generator[TestClient, None, None]:
    """Test client fixture."""

    config = get_settings_for_testing()
    with Session(bind=db_engine(config)) as db_session:
        reset_tables(db_session)
        add_sample_item(
            db_session,
            id=1, uuid='dummy', name='Sample item 1', description='1', )
        db_session.commit()

    def cleanup() -> None:
        with Session(bind=db_engine(config)) as db_session_:
            reset_tables(db_session_)
            db_session_.commit()

    request.addfinalizer(cleanup)

    with TestClient(app) as client_:
        yield client_

    with Session(bind=db_engine(config)) as db_session:
        reset_tables(db_session)
        db_session.commit()


def test_list_sample_items__verify_ok__returns_ok(
        client: TestClient,  # pylint: disable=redefined-outer-name
) -> None:
    """Test list AI models."""
    response = client.get(f'{API_BASE}/sample-items')
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    assert response.status_code == 200
    response_json = response.json()
    assert mock_overwrite_datetime(
        response_json, datetime(2025, 1, 1, 0, 0, 0)) == {
               'items': [
                   {
                       'uuid': 'dummy',
                       'name': 'Sample item 1',
                       'updated_at': '2025-01-01T00:00:00',
                       'deleted_at': None,
                       'created_at': '2025-01-01T00:00:00',
                       'description': '1'
                   }
               ],
               'total': 1,
               'page': 1,
               'size': 50,
               'pages': 1
           }
