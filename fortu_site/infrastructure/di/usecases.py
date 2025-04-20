from dishka import Provider, Scope, provide

from fortu_site.application.auth.use_cases import (
    UserRegisterUseCase,
    UserLoginUseCase,
    UserLogoutUseCase,
)


class UseCaseProvider(Provider):
    scope = Scope.REQUEST

    # auth
    register = provide(UserRegisterUseCase)
    login = provide(UserLoginUseCase)
    logout = provide(UserLogoutUseCase)
