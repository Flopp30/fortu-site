import dataclasses as dc
from io import BytesIO


@dc.dataclass
class InstallerIn:
    file_content: BytesIO
    file_name: str
    version: str
