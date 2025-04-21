import dataclasses as dc
import datetime


@dc.dataclass
class User:
    id: int = dc.field(init=False)
    name: str
    email: str
    password: str
    created_at: datetime.datetime = dc.field(init=False)
    is_admin: bool = False
