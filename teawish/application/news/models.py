import dataclasses as dc
import datetime

from teawish.application.user.models import USER_ID


@dc.dataclass
class News:
    title: str
    text: str
    created_at: datetime.datetime
    creator_id: USER_ID
    id: int | None = None
