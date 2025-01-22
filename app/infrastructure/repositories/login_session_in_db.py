"""LoginSession repository in database."""
from datetime import datetime
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.login_session import LoginSession
from app.domain.repositories.login_session import LoginSessionRepository
from app.infrastructure.repositories.base import InDBBaseEntityRepository


class InDBLoginSessionRepository(
    LoginSessionRepository,
    InDBBaseEntityRepository[str, LoginSession],
):
    """LoginSession repository in database."""
    _entity_cls = LoginSession

    @staticmethod
    def factory(
            get_now: Callable[[], datetime]
    ) -> Callable[[AsyncSession], 'InDBLoginSessionRepository']:
        """Factory method."""
        return lambda db_session: InDBLoginSessionRepository(db_session,
                                                             get_now)
