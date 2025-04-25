from dishka import Provider, from_context, Scope

from teawish.config import DatabaseConfig, AuthConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    db = from_context(DatabaseConfig)
    auth = from_context(AuthConfig)
