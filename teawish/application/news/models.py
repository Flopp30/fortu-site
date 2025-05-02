import dataclasses as dc
import datetime


@dc.dataclass
class News:
    title: str
    text: str
    created_at: datetime.datetime
    creator_id: int
    id: int | None = None
