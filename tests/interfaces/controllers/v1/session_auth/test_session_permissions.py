"""Test case for the list users endpoint."""
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.config import get_settings_for_testing
from app.domain.value_objects.role_permision import RoleName, PermissionName
from app.main import app
from tests.libs.mocks import add_user, add_login_session, \
    DUMMY_SESSION_ID1, DUMMY_SESSION_ID2, add_role, add_permission, \
    add_user_role, add_role_permission, DUMMY_SESSION_ID3, \
    add_default_super_user
from tests.libs.utils import init_and_autocommit_session, define_cleanup, \
    API_BASE


@pytest_asyncio.fixture(scope='function')
async def client(request: pytest.FixtureRequest) -> AsyncGenerator[
    AsyncClient, None]:
    """Test client fixture."""
    config = get_settings_for_testing()

    with init_and_autocommit_session(config) as db_session:
        add_default_super_user(db_session)
        add_user(
            db_session, uuid='dummy2', email='admin@fawapp.com',
            password_hash=config.pass_hash_for_test,
        )
        add_user(
            db_session, uuid='dummy3', email='user@fawapp.com',
            password_hash=config.pass_hash_for_test,
        )
        add_login_session(  # super
            db_session, id=DUMMY_SESSION_ID1,
            user_id=1, user_uuid='dummy',
        )
        add_login_session(  # admin
            db_session, id=DUMMY_SESSION_ID2,
            user_id=2, user_uuid='dummy2',
        )
        add_login_session(  # user
            db_session, id=DUMMY_SESSION_ID3,
            user_id=3, user_uuid='dummy3',
        )
        add_role(db_session, name=RoleName.ADMIN)
        add_role(db_session, name=RoleName.USER)
        add_permission(db_session, name=PermissionName.ADMIN_READ)
        db_session.flush()
        add_user_role(db_session, user_id=2, role_id=1)  # admin-admin
        add_user_role(db_session, user_id=3, role_id=2)  # user-user
        add_role_permission(db_session, role_id=1, permission_id=1)

    request.addfinalizer(define_cleanup(config))

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://test') as client_:
        yield client_


@pytest.mark.parametrize(
    'session_id, expected_status_code',
    [
        (DUMMY_SESSION_ID1, 200),
        (DUMMY_SESSION_ID2, 200),
        (DUMMY_SESSION_ID3, 403),
        ('no_exist_session_id', 401),
    ],
)
@pytest.mark.asyncio
async def test_session_auth_and_permissions(
        client: AsyncClient,  # pylint: disable=redefined-outer-name
        session_id: str, expected_status_code: int,
) -> None:
    """Test list users."""
    client.cookies.set('session', session_id)
    response = await client.get(
        f'{API_BASE}/admin/users/',
    )
    assert response.status_code == expected_status_code
