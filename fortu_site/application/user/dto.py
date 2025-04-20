import dataclasses as dc
import datetime


@dc.dataclass
class CreateUserIn:
    name: str
    email: str
    password: str


@dc.dataclass
class UserOut:
    id: int
    name: str
    email: str
    created_at: datetime.datetime
