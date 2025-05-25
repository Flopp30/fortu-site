import dataclasses as dc
from enum import Enum


class ServerStatus(Enum):
    online = 'online'
    offline = 'offline'


@dc.dataclass
class ServerInfo:
    status: ServerStatus = ServerStatus.offline
    online_users: int = 0
    total_users: int = 0
