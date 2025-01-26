"""Test the login endpoint."""
import json
import typing
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from freezegun import freeze_time
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings_for_testing
from app.domain.entities.login_session import LoginSession
from app.main import app
from tests.libs.utils import API_BASE, init_and_autocommit_session, \
    define_cleanup, mock_overwrite_datetime, add_super_user, db_engine


@pytest_asyncio.fixture(scope='function')
async def client(request: pytest.FixtureRequest) -> typing.AsyncGenerator[
    AsyncClient, None]:
    """Test client fixture."""
    config = get_settings_for_testing()

    with init_and_autocommit_session(config) as db_session:
        add_super_user(db_session)

    request.addfinalizer(define_cleanup(config))

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://test') as client_:
        yield client_


@pytest.mark.asyncio
@freeze_time('2025-01-02 00:00:00')
async def test_session_auth__verify_ok__return_ok(
        monkeypatch: pytest.MonkeyPatch,
        client: AsyncClient,  # pylint: disable=redefined-outer-name
) -> None:
    """Test session auth."""

    # TEST SESSION LOGIN ======================================================
    mock_session_id = 'mock_session_id'
    monkeypatch.setattr(
        'app.infrastructure.services.login_session.'
        'LoginSessionServiceImpl._generate_session_id',
        lambda *args, **kwargs: mock_session_id,
    )
    response = await client.post(
        f'{API_BASE}/auth/session/login',
        json={
            'username': 'admin@fawapp.com',
            'password': 'test123',
        },
    )
    assert response.status_code == 200
    assert 'session' in response.cookies
    session_id = response.cookies['session']
    assert session_id == mock_session_id
    config = get_settings_for_testing()

    with Session(bind=db_engine(config)) as db_session:
        session_entity: LoginSession = db_session.execute(
            select(LoginSession).where(
                LoginSession.id == session_id,  # type: ignore
            )
        ).scalars().one()

    assert mock_overwrite_datetime(
        session_entity.model_dump(),
        datetime(2025, 1, 1, 0, 0, 0),
    ) == {
               'id': session_id,
               'user_id': 1,
               'user_uuid': 'dummy',
               'expires_at': datetime(2025, 1, 9, 0, 0, 0,
                                      tzinfo=timezone.utc),
               'created_at': '2025-01-01T00:00:00',
               'updated_at': '2025-01-01T00:00:00',
               'deleted_at': None,
           }

    # TEST SESSION VERIFICATION ===============================================
    response2 = await client.get(
        f'{API_BASE}/auth/session/verify',
        cookies={'session': session_id},
    )
    print(json.dumps(response2.json(), indent=4, ensure_ascii=False))
    assert response2.status_code == 200
    assert mock_overwrite_datetime(
        response2.json(),
        datetime(2025, 1, 1, 0, 0, 0),
    ) == {
               'id': session_id,
               'user_id': 1,
               'user_uuid': 'dummy',
               'expires_at': '2025-01-09T00:00:00Z',
               'created_at': '2025-01-01T00:00:00',
               'updated_at': '2025-01-01T00:00:00',
               'deleted_at': None,
           }

    # TEST SESSION LOGOUT =====================================================
    response3 = await client.post(
        f'{API_BASE}/auth/session/logout',
        cookies={'session': session_id},
    )
    assert response3.status_code == 200
    assert 'session' not in response3.cookies

    with Session(bind=db_engine(config)) as db_session:
        not_found_session: LoginSession = db_session.execute(
            select(LoginSession).where(
                LoginSession.id == session_id,  # type: ignore
            )
        ).scalars().first()

        assert not_found_session is None
