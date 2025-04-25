import dataclasses as dc
import datetime
from uuid import UUID
from typing import TypeAlias

USER_ID: TypeAlias = UUID


@dc.dataclass
class User:
    id: USER_ID = dc.field(init=False)
    name: str
    email: str
    password: str
    created_at: datetime.datetime
    is_admin: bool = False
