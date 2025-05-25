import logging

from mcstatus import JavaServer
from mcstatus.responses import JavaStatusResponse

from teawish.application.game_server.dto import ServerInfo, ServerStatus
from teawish.application.game_server.interfaces import IGameServerClient

log = logging.getLogger(__name__)


class GameServerClient(IGameServerClient):
    def __init__(self, server: JavaServer):
        self.server: JavaServer = server

    def get_status(self) -> JavaStatusResponse:
        return self.server.status()

    def get_server_info(self) -> ServerInfo:
        try:
            status = self.get_status()
            return ServerInfo(
                status=ServerStatus.online,
                online_users=status.players.online,
                total_users=status.players.max,
            )
        except Exception as e:
            log.error(e)

        return ServerInfo()
