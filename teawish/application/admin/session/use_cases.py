import dataclasses as dc
import logging
from uuid import UUID

from teawish.application.admin.exceptions import AccessDenied
from teawish.application.auth.interfaces import ISessionRepository, SessionStorageFilter
from teawish.application.auth.models import Session
from teawish.application.user.models import User

log = logging.getLogger(__name__)


class AdminSessionListUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
    ):
        self._session_repository = session_repository

    async def __call__(self, session_id: UUID, limit: int, offset: int) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        sessions: list[Session] = await self._session_repository.get_list(limit=limit, offset=offset)
        total_count: int = await self._session_repository.total_count()

        context: dict = {
            'objects': sessions,
            'total_count': total_count,
        }

        return context
