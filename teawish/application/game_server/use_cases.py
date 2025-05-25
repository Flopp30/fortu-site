from teawish.application.game_server.dto import ServerInfo
from teawish.application.game_server.interfaces import IGameServerClient


class GetGameServerStatusUseCase:
    def __init__(
        self,
        game_server_client: IGameServerClient,
    ):
        self._server_client = game_server_client

    async def __call__(self) -> ServerInfo:
        return self._server_client.get_server_info()
