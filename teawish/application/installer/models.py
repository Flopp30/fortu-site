import dataclasses as dc
import datetime

from teawish.application.user.models import USER_ID


@dc.dataclass
class Installer:
    version: str
    file_path: str
    creator_id: USER_ID
    created_at: datetime.datetime | None = None
    id: int | None = None
