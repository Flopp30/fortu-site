import dataclasses as dc
import datetime
import logging
from pathlib import Path
from uuid import UUID

from teawish.application.admin.exceptions import AccessDenied
from teawish.application.auth.exceptions import ExpiredSessionException, OperationNotPermittedException
from teawish.application.auth.interfaces import (
    ISessionRepository,
    SessionStorageFilter,
)
from teawish.application.auth.models import SESSION_ID
from teawish.application.db import IUoW
from teawish.application.launcher.dto import LauncherIn
from teawish.application.launcher.interfaces import ILauncherFileStorage, ILauncherRepository
from teawish.application.launcher.models import Launcher
from teawish.application.user.exceptions import UserDoesNotExistsException
from teawish.application.user.models import User

log = logging.getLogger(__name__)


class AdminLauncherListUseCase:
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


class AdminLauncherFormUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
        launcher_repo: ILauncherRepository,
    ):
        self._session_repository = session_repository
        self._launcher_repo = launcher_repo

    async def __call__(self, session_id: UUID, launcher_id: int | None = None) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        context: dict = {}
        if launcher_id:
            launcher: Launcher = await self._launcher_repo.get(launcher_id)
            context['object'] = launcher

        return context


class AdminUpdateLauncherUseCase:
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
        # FIXME доделать

        return context


class AdminCreateLauncherUseCase:
    def __init__(
        self,
        uow: IUoW,
        launcher_repository: ILauncherRepository,
        session_repository: ISessionRepository,
        file_storage: ILauncherFileStorage,
    ):
        self._launcher_repository = launcher_repository
        self._session_repository = session_repository
        self._file_storage = file_storage
        self._uow = uow

    async def __call__(self, session_id: SESSION_ID, launcher_data: LauncherIn) -> Launcher:
        try:
            user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))
        except UserDoesNotExistsException:
            raise ExpiredSessionException('session expired')
        if not user.is_admin:
            raise OperationNotPermittedException
        file_name: str = f'{launcher_data.version}_{launcher_data.file_name}'
        file_path: Path = self._file_storage.save(launcher_data.file_content, file_name)

        launcher: Launcher = await self._launcher_repository.create(
            Launcher(
                file_path=str(file_path),
                created_at=datetime.datetime.now(),
                creator_id=user.id,
                version=launcher_data.version,
            )
        )
        await self._uow.commit()

        return launcher
