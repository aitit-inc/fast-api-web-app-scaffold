"""Test token login."""
import json
import typing

import pytest
import pytest_asyncio
from freezegun import freeze_time
from httpx import AsyncClient, ASGITransport
from jose import jwt

from app.config import get_settings_for_testing
from app.interfaces.middlewares.authorizer import AuthMethod
from app.main import app
from tests.libs.utils import API_BASE, init_and_autocommit_session, \
    define_cleanup, add_super_user


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
# @freeze_time('2025-01-02 00:00:00')
async def test_token_auth__verify_ok__return_ok(
        monkeypatch: pytest.MonkeyPatch,
        client: AsyncClient,  # pylint: disable=redefined-outer-name
) -> None:
    """Test token login."""
    with freeze_time('2025-01-02 00:00:00'):
        monkeypatch.setattr(
            'app.interfaces.middlewares.auth_middleware.'
            'AuthorizationMiddleware._auth_method',
            AuthMethod.BEARER_ACCESS_TOKEN,
        )

        response = await client.post(
            f'{API_BASE}/auth/token/',
            data={
                'grant_type': 'password',
                'username': 'admin@fawapp.com',
                'password': 'test123',
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        assert response.status_code == 200
        assert 'access_token' in response.json()
        assert 'refresh_token' in response.json()
        assert response.json()['token_type'] == 'bearer'
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        config = get_settings_for_testing()

        access_token_payload = jwt.decode(
            access_token,
            config.token_secret_key,
            algorithms=[config.token_algorithm],
            audience=config.audience,
            issuer=config.issuer,
        )
        assert access_token_payload == {
            'aud': 'https://fawapp.com',
            'email': 'admin@fawapp.com',
            'exp': 1735777800,
            'iat': 1735776000,
            'is_refresh_token': False,
            'iss': 'https://fawapp.com',
            'nbf': 1735776000,
            'sub': 'dummy',
        }

        refresh_token_payload = jwt.decode(
            refresh_token,
            config.token_secret_key,
            algorithms=[config.token_algorithm],
            audience=config.audience,
            issuer=config.issuer,
        )
        assert refresh_token_payload == {
            'aud': 'https://fawapp.com',
            'email': 'admin@fawapp.com',
            'exp': 1736380800,
            'iat': 1735776000,
            'is_refresh_token': True,
            'iss': 'https://fawapp.com',
            'nbf': 1735776000,
            'sub': 'dummy',
        }

        response2 = await client.get(
            f'{API_BASE}/auth/token/verify',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        print(json.dumps(response2.json(), indent=4, ensure_ascii=False))
        assert response2.status_code == 200
        assert response2.json() == {
            'aud': 'https://fawapp.com',
            'email': 'admin@fawapp.com',
            'exp': 1735777800,
            'exp_dt': '2025-01-02T00:30:00Z',
            'iat': 1735776000,
            'iat_dt': '2025-01-02T00:00:00Z',
            'is_refresh_token': False,
            'iss': 'https://fawapp.com',
            'jti': None,
            'nbf': 1735776000,
            'nbf_dt': '2025-01-02T00:00:00Z',
            'sub': 'dummy'
        }

    with freeze_time('2025-01-02 00:00:01'):
        response3 = await client.post(
            f'{API_BASE}/auth/token/refresh',
            headers={'Authorization': f'Bearer {refresh_token}'},
        )
        print(json.dumps(response3.json(), indent=4, ensure_ascii=False))
        assert response3.status_code == 200
        assert 'access_token' in response3.json()
        assert 'refresh_token' in response3.json()
        assert response3.json()['token_type'] == 'bearer'
        access_token3 = response3.json()['access_token']
        refresh_token3 = response3.json()['refresh_token']
        assert access_token3 != access_token
        assert refresh_token3 == refresh_token
