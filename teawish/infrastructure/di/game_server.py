from dishka import Provider, Scope, provide
from mcstatus import JavaServer

from teawish.application.game_server.interfaces import IGameServerClient
from teawish.config.config import GameServerConfig
from teawish.infrastructure.game_server.client import GameServerClient


class GameServerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_server(self, config: GameServerConfig) -> JavaServer:
        return JavaServer.lookup(f'{config.address}:{config.port}')

    @provide(scope=Scope.REQUEST, provides=IGameServerClient)
    def get_client(self, server: JavaServer) -> GameServerClient:
        return GameServerClient(server)
