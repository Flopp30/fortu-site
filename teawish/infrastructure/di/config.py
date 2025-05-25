from dishka import Provider, from_context, Scope

from teawish.config import DatabaseConfig, AuthConfig, AppConfig
from teawish.config.config import GameServerConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    db = from_context(DatabaseConfig)
    auth = from_context(AuthConfig)
    app = from_context(AppConfig)
    game_server = from_context(GameServerConfig)
