"""DI container."""
import logging

from dependency_injector import containers, providers

from app.domain.factories.sample_item import SampleItemFactory
from app.infrastructure.config import config
from app.infrastructure.database.database import Database
from app.infrastructure.repositories.sample_item_in_db import \
    InDBSampleItemRepository
from app.infrastructure.repositories.sample_item_in_memory import \
    InMemorySampleItemRepository

logger = logging.getLogger('uvicorn')


class Container(containers.DeclarativeContainer):
    """Container for DI."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            'app.interfaces.controllers.base',
            'app.interfaces.controllers.v1.base',

            # V1 app endpoints
            'app.interfaces.controllers.v1.sample_item',
        ],
    )

    get_settings = config.get_settings
    get_now = get_settings().get_now

    db = providers.Singleton(Database,
                             db_url=get_settings().db_dsn,
                             echo=get_settings().echo_sql)

    db_session_factory = providers.Factory(
        db.provided.session,
    )

    sample_item_factory = SampleItemFactory(get_now)
    # sample_item_repository = providers.Factory(
    #     InMemorySampleItemRepository,
    #     factory=sample_item_factory,
    # )
    sample_item_repository = providers.Object(
        InDBSampleItemRepository
    )
