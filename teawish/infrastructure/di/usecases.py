from dishka import Provider, Scope, provide

from teawish.application.admin.use_cases.admin import GetAdminPageUseCase
from teawish.application.admin.use_cases.launcher import GetLaunchersListPageUseCase, GetLaunchersFormPageUseCase, UpdateLaunchersPageUseCase
from teawish.application.admin.use_cases.news import CreateNewsFormPageUseCase, GetNewsListPageUseCase, GetNewsFormPageUseCase, UpdateNewsPageUseCase
from teawish.application.admin.use_cases.session import GetSessionListPageUseCase
from teawish.application.admin.use_cases.user import GetUsersListPageUseCase
from teawish.application.auth.use_cases import (
    UserRegisterUseCase,
    UserLoginUseCase,
    UserLogoutUseCase,
)
from teawish.application.launcher.use_cases import GetCurrentLauncherUseCase, AdminCreateLauncherUseCase
from teawish.application.news.use_cases import GetUserNewsUseCase, NonAuthorizedUserNews


class UseCaseProvider(Provider):
    scope = Scope.REQUEST

    # auth
    register = provide(UserRegisterUseCase)
    login = provide(UserLoginUseCase)
    logout = provide(UserLogoutUseCase)

    # business
    get_news = provide(GetUserNewsUseCase)
    get_current_launcher = provide(GetCurrentLauncherUseCase)

    # business api
    get_api_news = provide(NonAuthorizedUserNews)

    # admin
    create_launcher = provide(AdminCreateLauncherUseCase)
    get_admin_page = provide(GetAdminPageUseCase)
    get_users_list_page = provide(GetUsersListPageUseCase)
    get_launchers_list_page = provide(GetLaunchersListPageUseCase)
    get_launchers_form = provide(GetLaunchersFormPageUseCase)
    update_launchers_page = provide(UpdateLaunchersPageUseCase)
    get_news_list_news_page = provide(GetNewsListPageUseCase)
    get_news_news_form_page = provide(GetNewsFormPageUseCase)
    create_news_page = provide(CreateNewsFormPageUseCase)
    get_session_list_page = provide(GetSessionListPageUseCase)