from dishka import Provider, Scope, provide

from teawish.application.auth.use_cases import (
    UserRegisterUseCase,
    UserLoginUseCase,
    UserLogoutUseCase,
)
from teawish.application.news.usecases import GetUserNewsUseCase


class UseCaseProvider(Provider):
    scope = Scope.REQUEST

    # auth
    register = provide(UserRegisterUseCase)
    login = provide(UserLoginUseCase)
    logout = provide(UserLogoutUseCase)

    # business
    get_news = provide(GetUserNewsUseCase)
