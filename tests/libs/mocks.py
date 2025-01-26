"""Mock objects for testing."""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.domain.entities.login_session import LoginSession
from app.domain.entities.sample_item import SampleItem
from app.domain.entities.user import User, Role, Permission, UserRoles, \
    RolePermissions


def add_sample_item(
        db_session: Session,
        **kwargs: object,
) -> None:
    """Add a sample item to the database."""
    db_session.add(
        SampleItem(
            id=kwargs.get('id') or None,
            uuid=kwargs.get('uuid') or None,
            name=kwargs.get('name') or 'Sample name',
            description=kwargs.get('description') or 'Sample description',
            created_at=kwargs.get('created_at') or None,
            updated_at=kwargs.get('updated_at') or None,
            deleted_at=kwargs.get('deleted_at') or None,
        )
    )


def add_user(
        db_session: Session,
        **kwargs: object,
) -> None:
    """Add a user to the database."""
    db_session.add(
        User(
            id=kwargs.get('id') or None,
            uuid=kwargs.get('uuid'),
            email=kwargs.get('email') or '<EMAIL>',
            password_hash=kwargs.get('password') or '<PASSWORD_HASH>',
            is_active=kwargs.get('is_active') or True,
            is_superuser=kwargs.get('is_superuser') or False,
            last_login=kwargs.get('last_login') or None,
            created_at=kwargs.get('created_at') or None,
            updated_at=kwargs.get('updated_at') or None,
            deleted_at=kwargs.get('deleted_at') or None,
        )
    )


# Password hash value of "a" by using "dummy_key" key.
PASS_HASH__A__FOR_DUMMY_KEY = \
    '$2b$12$/E2zxYuB.vRZunSZuy7sM.D1v0Flo5xaNGdX99uBHOwM0dTRt2w/i'


def add_default_super_user(
        db_session: Session,
) -> None:
    """Add a default super user to the database."""
    add_user(
        db_session,
        uuid='dummy',
        email='super@fawapp.com',
        password_hash=PASS_HASH__A__FOR_DUMMY_KEY,
        is_superuser=True,
    )


def add_role(
        db_session: Session,
        **kwargs: object,
) -> None:
    """Add a role to the database."""
    db_session.add(
        Role(
            id=kwargs.get('id') or None,
            name=kwargs.get('name'),
        )
    )


def add_user_role(
        db_session: Session,
        user_id: int,
        role_id: int,
) -> None:
    """Add a user role to the database."""
    db_session.add(
        UserRoles(
            user_id=user_id,
            role_id=role_id,
        )
    )


def add_permission(
        db_session: Session,
        **kwargs: object,
) -> None:
    """Add a permission to the database."""
    db_session.add(
        Permission(
            id=kwargs.get('id') or None,
            name=kwargs.get('name'),
        )
    )


def add_role_permission(
        db_session: Session,
        role_id: int,
        permission_id: int,
) -> None:
    """Add a role permission to the database."""
    db_session.add(
        RolePermissions(
            role_id=role_id,
            permission_id=permission_id,
        )
    )


def add_login_session(
        db_session: Session,
        **kwargs: object,
) -> None:
    """Add a login session to the database."""
    db_session.add(
        LoginSession(
            id=kwargs.get('id'),
            user_id=kwargs.get('user_id'),
            user_uuid=kwargs.get('user_uuid'),
            expires_at=kwargs.get('expires_at') or datetime(
                9999, 12, 31,
                tzinfo=timezone.utc),
            created_at=kwargs.get('created_at') or None,
            updated_at=kwargs.get('updated_at') or None,
            deleted_at=kwargs.get('deleted_at') or None,
        )
    )


DUMMY_SESSION_ID1 = 'dummy_session_id1'
DUMMY_SESSION_ID2 = 'dummy_session_id2'
DUMMY_SESSION_ID3 = 'dummy_session_id3'
