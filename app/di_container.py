"""DI container."""
import logging

from dependency_injector import containers, providers
from shortuuid import uuid

from app.domain.factories.auth import JwtPayloadFactory
from app.domain.factories.sample_item import SampleItemFactory
from app.infrastructure.config import config
from app.infrastructure.database.database import Database
from app.infrastructure.repositories.sample_item_in_db import \
    InDBSampleItemRepository, InDBSampleItemQueryFactory, \
    InDBSampleItemByUUIDRepository
from app.infrastructure.repositories.user_in_db import InDBUserRepository, \
    InDBUserByEmailRepository, InDBUserByUUIDRepository, InDBUserQueryFactory
from app.infrastructure.services.auth import InDBUserAuthService, \
    JwtTokenServiceImpl

logger = logging.getLogger('uvicorn')


class Container(containers.DeclarativeContainer):
    """Container for DI."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            'app.interfaces.controllers.base',
            'app.interfaces.controllers.v1.base',

            # V1 app endpoints
            'app.interfaces.controllers.v1.auth',
            'app.interfaces.controllers.v1.sample_item',
            'app.interfaces.controllers.v1.sample_item_by_uuid',

            # V1 app admin endpoints
            'app.interfaces.controllers.v1.admin.user',
        ],
    )

    get_settings = config.get_settings
    conf = get_settings()

    get_now = conf.get_now

    db = providers.Singleton(Database,
                             db_url=conf.db_dsn,
                             echo=conf.echo_sql)

    db_session_factory = providers.Factory(
        # pylint: disable=no-member
        db.provided.session,
    )

    sample_item_factory = SampleItemFactory(get_now, uuid)
    sample_item_repository = providers.Factory(
        InDBSampleItemRepository.factory,
        get_now=get_now,
    )
    sample_item_by_uuid_repository = providers.Factory(
        InDBSampleItemByUUIDRepository.factory,
        get_now=get_now,
    )
    sample_item_query_factory = providers.Factory(
        InDBSampleItemQueryFactory,
    )

    user_repository = providers.Factory(
        InDBUserRepository.factory,
        get_now=get_now,
    )
    user_by_email_repository = providers.Factory(
        InDBUserByEmailRepository.factory,
        get_now=get_now,
    )
    user_by_uuid_repository = providers.Factory(
        InDBUserByUUIDRepository.factory,
        get_now=get_now,
    )
    user_query_factory = providers.Factory(
        InDBUserQueryFactory,
    )

    user_auth_service_factory = providers.Factory(
        InDBUserAuthService.create_factory,
        get_now=get_now,
    )
    jwt_payload_factory = providers.Factory(
        JwtPayloadFactory,
        issuer=conf.issuer,
        audience=conf.audience,
        access_token_expire_minutes=conf.access_token_expire_minutes,
        refresh_token_expire_minutes=conf.refresh_token_expire_minutes,
        get_now=get_now,
    )
    jwt_token_service = providers.Factory(
        JwtTokenServiceImpl,
        token_secret_key=conf.token_secret_key,
        token_algorithm=conf.token_algorithm,
        issuer=conf.issuer,
        audience=conf.audience,
    )
