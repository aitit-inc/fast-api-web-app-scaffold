"""Test cases for the get sample item endpoint."""
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings_for_testing
from app.domain.entities.sample_item import SampleItem
from app.main import app
from tests.libs.mocks import add_sample_item
from tests.libs.utils import API_BASE, init_and_autocommit_session, \
    define_cleanup, db_engine


@pytest_asyncio.fixture(scope='function')
async def client(request: pytest.FixtureRequest) -> AsyncGenerator[
    AsyncClient, None]:
    """Test client fixture."""
    config = get_settings_for_testing()

    with init_and_autocommit_session(config) as db_session:
        add_sample_item(
            db_session,
            id=1, uuid='dummy', name='Sample item 1', description='1',
        )

    request.addfinalizer(define_cleanup(config))

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://test') as client_:
        yield client_


@pytest.mark.asyncio
async def test_logical_delete_sample_item__verify_ok__returns_ok(
        client: AsyncClient,  # pylint: disable=redefined-outer-name
) -> None:
    response = await client.delete(
        f'{API_BASE}/public/sample-items/1/physical')
    assert response.status_code == 204

    config = get_settings_for_testing()
    with Session(bind=db_engine(config)) as db_session:
        stmt = select(SampleItem).where(
            SampleItem.id == 1,
        )
        sample_item = db_session.scalars(stmt).first()

        assert sample_item is None

    return 'ok'
