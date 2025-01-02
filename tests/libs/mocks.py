"""Mock objects for testing."""

from sqlalchemy.orm import Session

from app.domain.entities.sample_item import SampleItem


def add_sample_item(
        db_session: Session,
        **kwargs: object,
) -> None:
    """Add a sample item to the database."""
    db_session.add(
        SampleItem(
            id=kwargs.get('id') or None,
            name=kwargs.get('name') or 'Sample name',
            description=kwargs.get('description') or 'Sample description',
            is_deleted=kwargs.get('is_deleted') or False,
            created_at=kwargs.get('created_at') or None,
            updated_at=kwargs.get('updated_at') or None,
            deleted_at=kwargs.get('deleted_at') or None,
        )
    )
