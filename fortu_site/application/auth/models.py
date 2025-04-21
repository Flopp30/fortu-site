import dataclasses as dc
import datetime
from uuid import UUID


@dc.dataclass
class Session:
    user_id: int
    id: UUID | None = None
    created_at: datetime.datetime | None = None
    expires_at: datetime.datetime | None = None
