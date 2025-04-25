import dataclasses as dc
import datetime

from teawish.application.user.models import USER_ID


@dc.dataclass
class CreateUserIn:
    name: str
    email: str
    password: str


@dc.dataclass
class UserOut:
    id: USER_ID
    name: str
    email: str
    created_at: datetime.datetime
