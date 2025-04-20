from dishka import Provider, from_context, Scope

from fortu_site.config import DatabaseConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    db = from_context(DatabaseConfig)
