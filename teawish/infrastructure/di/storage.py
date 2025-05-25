from dishka import Provider, Scope, provide

from teawish.application.installer.interfaces import IInstallerFileStorage
from teawish.application.launcher.interfaces import ILauncherFileStorage
from teawish.config.config import AppConfig
from teawish.infrastructure.storages.in_memory import InstallerFileStorage, LauncherFileStorage


class StoragesProvider(Provider):
    scope = Scope.APP

    @provide
    def get_launcher_installer(self, app_config: AppConfig) -> ILauncherFileStorage:
        return LauncherFileStorage(app_config)

    @provide
    def get_installer_storage(self, app_config: AppConfig) -> IInstallerFileStorage:
        return InstallerFileStorage(app_config)
