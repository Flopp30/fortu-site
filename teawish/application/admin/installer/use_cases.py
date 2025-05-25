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
from teawish.application.installer.dto import InstallerIn
from teawish.application.installer.interfaces import IInstallerFileStorage, IInstallerRepository
from teawish.application.installer.models import Installer
from teawish.application.user.exceptions import UserDoesNotExistsException
from teawish.application.user.models import User

log = logging.getLogger(__name__)


class AdminInstallerListUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
        installer_repository: IInstallerRepository,
    ):
        self._session_repository = session_repository
        self._installer_repository = installer_repository

    async def __call__(self, session_id: UUID, limit: int, offset: int) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        installers: list[Installer] = await self._installer_repository.get_list(limit, offset)
        total_count: int = await self._installer_repository.total_count()

        return {
            'objects': installers,
            'total_count': total_count,
        }


class AdminInstallerFormUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
        installer_repository: IInstallerRepository,
    ):
        self._session_repository = session_repository
        self._installer_repository = installer_repository

    async def __call__(self, session_id: UUID, installer_id: int | None = None) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        context: dict = {}
        if installer_id:
            installer: Installer = await self._installer_repository.get(installer_id)
            context['object'] = installer

        return context


class AdminUpdateInstallerUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
        installer_repo: IInstallerRepository,
        file_storage: IInstallerFileStorage,
    ):
        self._session_repository = session_repository
        self._installer_repository = installer_repo
        self._file_storage = file_storage

    async def __call__(self, session_id: UUID, installer_id: int, version: str) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        context: dict = {}
        # installer: Installer = await self._installer_repository.get(installer_id)
        # file_bytes: BytesIO = file_storage.load(installer.file_path)
        # FIXME доделать

        return context


class AdminCreateInstallerUseCase:
    def __init__(
        self,
        uow: IUoW,
        installer_repository: IInstallerRepository,
        session_repository: ISessionRepository,
        file_storage: IInstallerFileStorage,
    ):
        self._installer_repository = installer_repository
        self._session_repository = session_repository
        self._file_storage = file_storage
        self._uow = uow

    async def __call__(self, session_id: SESSION_ID, installer_data: InstallerIn) -> Installer:
        try:
            user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))
        except UserDoesNotExistsException:
            raise ExpiredSessionException('session expired')
        if not user.is_admin:
            raise OperationNotPermittedException
        file_name: str = f'{installer_data.version}_{installer_data.file_name}'
        file_path: Path = self._file_storage.save(installer_data.file_content, file_name)
        log.info(f'file path: {file_path}')
        log.info(f'file name: {file_name}')
        installer: Installer = await self._installer_repository.create(
            Installer(
                file_path=str(file_path.absolute()),
                created_at=datetime.datetime.now(),
                creator_id=user.id,
                version=installer_data.version,
            )
        )
        await self._uow.commit()

        return installer
