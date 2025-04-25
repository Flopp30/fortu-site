from dishka import Provider, Scope, provide

from teawish.application.auth.use_cases import (
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
