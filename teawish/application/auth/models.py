import dataclasses as dc
import datetime
from typing import TypeAlias
from uuid import UUID

from teawish.application.user.models import USER_ID

SESSION_ID: TypeAlias = UUID


@dc.dataclass
class Session:
    user_id: USER_ID
    expired_at: datetime.datetime
    created_at: datetime.datetime
    id: SESSION_ID | None = None
