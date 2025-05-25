import logging

from teawish.application.installer.exceptions import InstallerDoesNotExistsException
from teawish.application.installer.interfaces import IInstallerRepository
from teawish.application.installer.models import Installer

log = logging.getLogger(__name__)


class GetCurrentInstallerUseCase:
    def __init__(
        self,
        installer_repository: IInstallerRepository,
    ):
        self._installer_repository = installer_repository

    async def __call__(self) -> Installer | None:
        try:
            return await self._installer_repository.get_current()
        except InstallerDoesNotExistsException:
            log.warning('Installer not found')
        return None
