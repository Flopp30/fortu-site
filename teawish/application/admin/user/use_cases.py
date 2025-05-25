import dataclasses as dc
import logging
from uuid import UUID

from teawish.application.admin.exceptions import AccessDenied
from teawish.application.auth.interfaces import (
    ISessionRepository,
    SessionStorageFilter,
)
from teawish.application.user.interfaces import IUserRepository
from teawish.application.user.models import User

log = logging.getLogger(__name__)


class AdminUsersListUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        session_repository: ISessionRepository,
    ):
        self._user_repository = user_repository
        self._session_repository = session_repository

    async def __call__(self, session_id: UUID, limit: int, offset: int) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        users: list[User] = await self._user_repository.get_list(limit, offset)
        total_count: int = await self._user_repository.total_count()

        return {
            'objects': users,
            'total_count': total_count,
        }
