import logging

from teawish.application.launcher.exceptions import LauncherDoesNotExistsException
from teawish.application.launcher.interfaces import ILauncherRepository
from teawish.application.launcher.models import Launcher

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
