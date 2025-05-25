from typing import Protocol

from teawish.application.game_server.dto import ServerInfo


class IGameServerClient(Protocol):
    def get_server_info(self) -> ServerInfo: ...
