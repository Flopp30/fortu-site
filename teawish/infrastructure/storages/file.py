import os.path
from io import BytesIO
from pathlib import Path

from teawish.application.launcher.interfaces import ILauncherFileStorage
from teawish.config import AppConfig


class LauncherFileStorage(ILauncherFileStorage):
    def __init__(self, app_config: AppConfig):
        base_path: str = app_config.file_dir
        self.file_path: Path = Path(base_path) / 'launchers'
        os.makedirs(self.file_path, exist_ok=True)

    def save(self, content: BytesIO, file_name: str) -> Path:
        file_path = self.file_path / file_name
        with open(file_path, 'wb') as f:
            f.write(content.getbuffer())
        return file_path

    def load(self, file_path: str) -> BytesIO:
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise FileNotFoundError

        with open(file_path, 'rb') as f:
            content = f.read()
        return BytesIO(content)
