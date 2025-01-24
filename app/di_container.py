"""DI container."""
import logging

from dependency_injector import containers, providers
from shortuuid import uuid

from app import config
from app.application.dto.session_auth import SessionCookieConfig, SameSite
from app.domain.factories.sample_item import SampleItemFactory
from app.domain.factories.token_auth import JwtPayloadFactory
from app.infrastructure.database.database import Database
from app.infrastructure.repositories.login_session_in_db import \
    InDBLoginSessionRepository
from app.infrastructure.repositories.sample_item_in_db import \
    InDBSampleItemRepository, InDBSampleItemQueryFactory, \
    InDBSampleItemByUUIDRepository
from app.infrastructure.repositories.user_in_db import InDBUserRepository, \
    InDBUserByEmailRepository, InDBUserByUUIDRepository, InDBUserQueryFactory
from app.infrastructure.services.login_session import LoginSessionServiceImpl
from app.infrastructure.services.token_auth import InDBUserTokenAuthService, \
    JwtTokenServiceImpl
from app.interfaces.middlewares.authorizer import AccessTokenAuthorizer, \
    SessionCookieAuthorizer

logger = logging.getLogger('uvicorn')


class Container(containers.DeclarativeContainer):
    """Container for DI."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            'app.interfaces.controllers.base',
            'app.interfaces.controllers.v1.base',

            # V1 app endpoints
            'app.interfaces.controllers.v1.token_auth',
            'app.interfaces.controllers.v1.session_auth',
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
        InDBUserTokenAuthService.create_factory,
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

    login_session_repository_factory = providers.Factory(
        InDBLoginSessionRepository.factory,
        get_now=get_now,
    )
    login_session_service = providers.Factory(
        LoginSessionServiceImpl,
        login_session_secret_key=conf.login_session_secret_key,
        login_session_expire_minutes=conf.login_session_expire_minutes,
        get_now=get_now,
        uuid_gen=uuid,
    )
    login_session_cookie_name = providers.Object(
        conf.login_session_cookie_name,
    )
    _session_cookie_config = SessionCookieConfig(
        key=conf.login_session_cookie_name,
        httponly=conf.login_session_cookie_httponly,
        max_age=conf.login_session_expire_minutes * 60,
        samesite=SameSite(conf.login_session_cookie_samesite),
        secure=conf.login_session_cookie_secure,
    )
    session_cookie_config = providers.Object(_session_cookie_config)

    access_token_authorizer = providers.Factory(
        AccessTokenAuthorizer,
        jwt_token_service=jwt_token_service,
    )
    session_cookie_authorizer_factory = providers.Factory(
        SessionCookieAuthorizer.create_factory,
        login_session_repository_factory=login_session_repository_factory,
        login_session_service=login_session_service,
        login_session_cookie_name=conf.login_session_cookie_name,
    )
