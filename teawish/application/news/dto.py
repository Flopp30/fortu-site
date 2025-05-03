import dataclasses as dc
import datetime


@dc.dataclass
class UserNewsOut:
    title: str
    text: str
    created_at: datetime.datetime
    id: int
