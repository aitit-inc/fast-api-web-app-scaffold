"""Test cases for the get sample item endpoint."""
import json
from datetime import datetime
from typing import AsyncGenerator, Any

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.config import get_settings_for_testing
from app.main import app
from tests.libs.mocks import add_sample_item
from tests.libs.utils import API_BASE, mock_overwrite_datetime, \
    init_and_autocommit_session, define_cleanup


@pytest_asyncio.fixture(scope='function')
async def client(request: pytest.FixtureRequest) -> AsyncGenerator[
    AsyncClient, None]:
    """Test client fixture."""
    config = get_settings_for_testing()

    with init_and_autocommit_session(config) as db_session:
        add_sample_item(
            db_session,
            uuid='dummy', name='Sample item 1', description='1',
        )

    request.addfinalizer(define_cleanup(config))

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://test') as client_:
        yield client_


@pytest.mark.parametrize(
    'query, expected',
    [
        ({}, {
            'name': 'Sample item 1',
            'description': '1',
            'uuid': 'dummy',
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00',
            'deleted_at': None,
        }),
        ({'with_meta': True}, {
            'name': 'Sample item 1',
            'description': '1',
            'uuid': 'dummy',
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00',
            'deleted_at': None,
            'meta_data': {
                'name_length': 13,
                'description_length': 1,
            },
        }),
    ],
)
@pytest.mark.asyncio
async def test_get_sample_item__verify_ok__returns_ok(
        client: AsyncClient,  # pylint: disable=redefined-outer-name
        query: dict[str, Any], expected: dict[str, Any],
) -> None:
    """Test get sample item."""
    response = await client.get(
        f'{API_BASE}/public/sample-items/1',
        params=query, )
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    assert response.status_code == 200
    response_json = response.json()
    assert mock_overwrite_datetime(
        response_json,
        datetime(2025, 1, 1, 0, 0, 0)
    ) == expected
