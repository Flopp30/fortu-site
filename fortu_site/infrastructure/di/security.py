from dishka import Provider, Scope, provide

from fortu_site.application.auth.interfaces import IPasswordEncryptor, IAuthSessionService
from fortu_site.infrastructure.security.auth import AuthSessionService
from fortu_site.infrastructure.security.password import PasswordEncryptor


class SecurityProvider(Provider):
    scope = Scope.APP

    password = provide(PasswordEncryptor, provides=IPasswordEncryptor)
    session = provide(AuthSessionService, provides=IAuthSessionService)
