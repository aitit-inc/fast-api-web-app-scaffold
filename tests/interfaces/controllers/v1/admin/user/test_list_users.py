"""Test case for the list users endpoint."""
import json
from datetime import datetime
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.config import get_settings_for_testing
from app.main import app
from tests.libs.mocks import add_login_session, \
    DUMMY_SESSION_ID1, add_default_super_user
from tests.libs.utils import init_and_autocommit_session, define_cleanup, \
    API_BASE, mock_overwrite_datetime


@pytest_asyncio.fixture(scope='function')
async def client(request: pytest.FixtureRequest) -> AsyncGenerator[
    AsyncClient, None]:
    """Test client fixture."""
    config = get_settings_for_testing()

    with init_and_autocommit_session(config) as db_session:
        add_default_super_user(db_session)
        add_login_session(
            db_session, id=DUMMY_SESSION_ID1,
            user_id=1, user_uuid='dummy',
        )

    request.addfinalizer(define_cleanup(config))

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://test') as client_:
        yield client_


@pytest.mark.asyncio
async def test_list_users__verify_ok__return_ok(
        client: AsyncClient,  # pylint: disable=redefined-outer-name
) -> None:
    """Test list users."""
    client.cookies.set('session', DUMMY_SESSION_ID1)
    response = await client.get(
        f'{API_BASE}/admin/users/',
    )
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    assert response.status_code == 200
    response_json = response.json()
    assert mock_overwrite_datetime(
        response_json, datetime(2025, 1, 1, 0, 0, 0),
    ) == {
               'items': [
                   {
                       'first_name': None,
                       'last_name': None,
                       'email': 'super@fawapp.com',
                       'uuid': 'dummy',
                       'is_active': True,
                       'is_superuser': True,
                       'last_login': None,
                       'created_at': '2025-01-01T00:00:00',
                       'updated_at': '2025-01-01T00:00:00',
                       'deleted_at': None
                   },
               ],
               'total': 1,
               'page': 1,
               'size': 50,
               'pages': 1
           }
