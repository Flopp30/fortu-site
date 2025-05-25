import dataclasses as dc
import logging
from uuid import UUID

from teawish.application.admin.exceptions import AccessDenied
from teawish.application.auth.interfaces import (
    ISessionRepository,
    SessionStorageFilter,
)
from teawish.application.user.models import User

log = logging.getLogger(__name__)


class GetAdminPageUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
    ):
        self._session_repository = session_repository

    async def __call__(self, session_id: UUID) -> User:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        return user
