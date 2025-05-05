from dishka import Provider, provide, Scope

from teawish.application.launcher.interfaces import ILauncherFileStorage
from teawish.infrastructure.storages.file import LauncherFileStorage


class StoragesProvider(Provider):
    scope = Scope.APP
    file_storage = provide(LauncherFileStorage, provides=ILauncherFileStorage)
