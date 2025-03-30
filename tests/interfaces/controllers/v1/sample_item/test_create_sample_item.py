"""Test case for the create sample item endpoint."""
import json
from datetime import datetime
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.config import get_settings_for_testing
from app.main import app
from tests.libs.utils import API_BASE, init_and_autocommit_session, \
    define_cleanup, mock_overwrite_datetime


@pytest_asyncio.fixture(scope='function')
async def client(request: pytest.FixtureRequest) -> AsyncGenerator[
    AsyncClient, None]:
    """Test client fixture."""
    config = get_settings_for_testing()

    with init_and_autocommit_session(config):
        # just reset db
        pass

    request.addfinalizer(define_cleanup(config))

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://test') as client_:
        yield client_


@pytest.mark.asyncio
async def test_create_sample_item__verify_ok__return_ok(
        monkeypatch: pytest.MonkeyPatch,
        client: AsyncClient,  # pylint: disable=redefined-outer-name
) -> None:
    """Test create sample item."""

    monkeypatch.setattr(
        'app.application.use_cases.sample_item.create.'
        'SampleItemCreateUseCase._gen_uuid',
        lambda *args, **kwargs: 'dummy',
    )
    response = await client.post(
        f'{API_BASE}/public/sample-items',
        json={'name': 'Sample item 1',
              'description': '1'},
    )
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    assert response.status_code == 201
    response_json = response.json()
    assert mock_overwrite_datetime(
        response_json,
        datetime(2025, 1, 1, 0, 0, 0),
    ) == {
               'name': 'Sample item 1',
               'description': '1',
               'uuid': 'dummy',
               'created_at': '2025-01-01T00:00:00',
               'updated_at': '2025-01-01T00:00:00',
               'deleted_at': None,
           }
