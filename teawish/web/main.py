import datetime

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from teawish.config import DatabaseConfig, WebConfig, AppConfig, AuthConfig
from teawish.infrastructure.di.config import ConfigProvider
from teawish.infrastructure.di.database import RepositoriesProvider, DatabaseProvider
from teawish.infrastructure.di.security import SecurityProvider
from teawish.infrastructure.di.storage import StoragesProvider
from teawish.infrastructure.di.usecases import UseCaseProvider
from teawish.infrastructure.logging import setup_logging
from teawish.web.api_routers import setup_api_routers
from teawish.web.exceptions import setup_exception_handlers
from teawish.web.middlewares import TimingMiddleware
from teawish.web.template_routers import setup_template_routers


def create_app() -> FastAPI:
    app_config: AppConfig = AppConfig.from_env()
    setup_logging()
    app = FastAPI(
        title='Fortu-site',
        version='0.1.0',
        default_response_class=ORJSONResponse,
    )

    web_config: WebConfig = WebConfig.from_env()
    templates: Jinja2Templates = get_templates(web_config)
    # DI контейнер
    setup_ioc_container(app, templates, app_config)
    # обработчики исключений
    setup_exception_handlers(app, templates)
    # middlewares
    setup_middlewares(app, app_config)
    # статика
    setup_static(app, web_config)
    # роутеры с шаблонами
    setup_template_routers(app)
    # апи роутеры
    setup_api_routers(app)
    return app


def setup_middlewares(app: FastAPI, app_config: AppConfig):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.cors_origins,
        allow_credentials=True,
        allow_methods=app_config.allow_methods,
        allow_headers=app_config.allow_headers,
    )
    app.add_middleware(TimingMiddleware)


def setup_ioc_container(app: FastAPI, templates: Jinja2Templates, app_config: AppConfig) -> AsyncContainer:
    container: AsyncContainer = make_async_container(
        ConfigProvider(),
        SecurityProvider(),
        DatabaseProvider(),
        UseCaseProvider(),
        RepositoriesProvider(),
        StoragesProvider(),
        context={
            # config
            DatabaseConfig: DatabaseConfig.from_env(),
            AuthConfig: AuthConfig.from_env(),
            AppConfig: app_config,
            # templates
            Jinja2Templates: templates,
        },
    )

    setup_dishka(container, app)
    return container


def get_templates(web_config: WebConfig) -> Jinja2Templates:
    templates = Jinja2Templates(
        directory=web_config.templates_dir,
    )
    register_filters(templates, web_config)
    return templates


def register_filters(templates: Jinja2Templates, web_config: WebConfig):
    templates.env.globals['now'] = datetime.datetime.now
    templates.env.filters['format_date'] = lambda dt: dt.strftime('%H:%M %d.%m.%Y')
    templates.env.globals['discord_link'] = web_config.discord_link


def setup_static(app: FastAPI, web_config: WebConfig):
    app.mount(
        web_config.static_path,
        StaticFiles(
            directory=web_config.static_dir,
        ),
        name='static',
    )
