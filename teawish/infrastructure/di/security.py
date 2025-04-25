from dishka import Provider, Scope, provide

from teawish.application.auth.interfaces import IPasswordEncryptor, IAuthSessionService
from teawish.infrastructure.security.auth import AuthSessionService
from teawish.infrastructure.security.password import PasswordEncryptor


class SecurityProvider(Provider):
    scope = Scope.APP

    password = provide(PasswordEncryptor, provides=IPasswordEncryptor)
    session = provide(AuthSessionService, provides=IAuthSessionService)
