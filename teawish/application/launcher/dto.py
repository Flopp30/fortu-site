import dataclasses as dc
from io import BytesIO


@dc.dataclass
class LauncherIn:
    file_content: BytesIO
    file_name: str
    version: str
