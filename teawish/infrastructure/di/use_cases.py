from dishka import Provider, Scope, provide

from teawish.application.admin.common.use_cases import GetAdminPageUseCase
from teawish.application.admin.installer.use_cases import (
    AdminCreateInstallerUseCase,
    AdminInstallerFormUseCase,
    AdminInstallerListUseCase,
    AdminUpdateInstallerUseCase,
)
from teawish.application.admin.launcher.use_cases import (
    AdminCreateLauncherUseCase,
    AdminLauncherFormUseCase,
    AdminLauncherListUseCase,
    AdminUpdateLauncherUseCase,
)
from teawish.application.admin.news.use_cases import (
    AdminCreateNewsUseCase,
    AdminNewsFormUseCase,
    AdminNewsListUseCase,
    AdminUpdateNewsUseCase,
)
from teawish.application.admin.session.use_cases import AdminSessionListUseCase
from teawish.application.admin.user.use_cases import AdminUsersListUseCase
from teawish.application.auth.use_cases import (
    UserLoginUseCase,
    UserLogoutUseCase,
    UserRegisterUseCase,
)
from teawish.application.game_server.use_cases import GetGameServerStatusUseCase
from teawish.application.installer.use_cases import GetCurrentInstallerUseCase
from teawish.application.launcher.use_cases import GetCurrentLauncherUseCase
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
    get_current_installer = provide(GetCurrentInstallerUseCase)
    get_server_info = provide(GetGameServerStatusUseCase)

    # business api
    get_api_news = provide(NonAuthorizedUserNews)

    # admin
    get_admin = provide(GetAdminPageUseCase)
    # - users
    admin_get_users_list = provide(AdminUsersListUseCase)
    # - launcher
    admin_get_launchers_list_page = provide(AdminLauncherListUseCase)
    admin_get_launchers_form = provide(AdminLauncherFormUseCase)
    admin_create_launcher = provide(AdminCreateLauncherUseCase)
    admin_update_launchers = provide(AdminUpdateLauncherUseCase)
    # - news
    admin_get_news_list_news = provide(AdminNewsListUseCase)
    admin_get_news_form = provide(AdminNewsFormUseCase)
    admin_create_news = provide(AdminCreateNewsUseCase)
    admin_update_news = provide(AdminUpdateNewsUseCase)

    # - session
    get_session_list_page = provide(AdminSessionListUseCase)
    # - installer
    admin_get_installers_list = provide(AdminInstallerListUseCase)
    admin_get_installers_form = provide(AdminInstallerFormUseCase)
    admin_create_installer = provide(AdminCreateInstallerUseCase)
    admin_update_installers = provide(AdminUpdateInstallerUseCase)
