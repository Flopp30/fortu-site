from dishka import Provider, Scope, provide

from fortu_site.application.auth.interfaces import IPasswordEncryptor
from fortu_site.infrastructure.security.password import PasswordEncryptor


class SecurityProvider(Provider):
    scope = Scope.APP

    password = provide(PasswordEncryptor, provides=IPasswordEncryptor)
