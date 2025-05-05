import datetime
import logging
from pathlib import Path

from teawish.application.auth.exceptions import ExpiredSessionException, OperationNotPermittedException
from teawish.application.auth.interfaces import ISessionRepository, SessionStorageFilter
from teawish.application.auth.models import SESSION_ID
from teawish.application.db import IUoW
from teawish.application.launcher.dto import LauncherIn
from teawish.application.launcher.exception import LauncherDoesNotExistsException
from teawish.application.launcher.interfaces import ILauncherRepository, ILauncherFileStorage
from teawish.application.launcher.models import Launcher
from teawish.application.user.exceptions import UserDoesNotExistsException
from teawish.application.user.models import User

log = logging.getLogger(__name__)


class GetCurrentLauncherUseCase:
    def __init__(
        self,
        launcher_repository: ILauncherRepository,
    ):
        self._launcher_repository = launcher_repository

    async def __call__(self) -> Launcher | None:
        try:
            return await self._launcher_repository.get_current()
        except LauncherDoesNotExistsException:
            log.warning('Launcher not found')
        return None


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
