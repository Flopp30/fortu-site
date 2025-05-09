import dataclasses as dc
import logging
from uuid import UUID

from teawish.application.admin.exceptions import AccessDenied
from teawish.application.auth.interfaces import (
    ISessionRepository,
    SessionStorageFilter,
)
from teawish.application.launcher.interfaces import ILauncherRepository, ILauncherFileStorage
from teawish.application.launcher.models import Launcher
from teawish.application.user.models import User

log = logging.getLogger(__name__)


class GetLaunchersListPageUseCase:
    def __init__(
            self,
            session_repository: ISessionRepository,
            launcher_repo: ILauncherRepository,
    ):
        self._session_repository = session_repository
        self._launcher_repo = launcher_repo

    async def __call__(self, session_id: UUID, limit: int, offset: int) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        launchers: list[Launcher] = await self._launcher_repo.get_list(limit, offset)
        total_count: int = await self._launcher_repo.total_count()

        return {
            'objects': launchers,
            'total_count': total_count,
        }


class GetLaunchersFormPageUseCase:
    def __init__(
            self,
            session_repository: ISessionRepository,
            launcher_repo: ILauncherRepository,
    ):
        self._session_repository = session_repository
        self._launcher_repo = launcher_repo

    async def __call__(self, session_id: UUID, launcher_id: int) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        context: dict = {}
        if launcher_id:
            launcher: Launcher = await self._launcher_repo.get(launcher_id)
            context['object'] = launcher

        return context


class UpdateLaunchersPageUseCase:
    def __init__(
            self,
            session_repository: ISessionRepository,
            session_repo: ISessionRepository,
            launcher_repo: ILauncherRepository,
            file_storage: ILauncherFileStorage,
    ):
        self._session_repository = session_repository

    async def __call__(self, session_id: UUID, launcher_id: int, version: str) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        context: dict = {}
        # launcher: Launcher = await launcher_repo.get(launcher_id)
        # file_bytes: BytesIO = file_storage.load(launcher.file_path)
        # fixme доделать

        return context
