from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from teawish.config import DatabaseConfig, WebConfig, ApiConfig, AuthConfig
from teawish.infrastructure.di.config import ConfigProvider
from teawish.infrastructure.di.database import RepositoriesProvider, DatabaseProvider
from teawish.infrastructure.di.security import SecurityProvider
from teawish.infrastructure.di.usecases import UseCaseProvider
from teawish.infrastructure.logging import setup_logging
from teawish.web.api_routers import setup_api_routers
from teawish.web.exceptions import setup_exception_handlers
from teawish.web.middlewares import TimingMiddleware
from teawish.web.template_routers import setup_template_routers


def create_app() -> FastAPI:
    api_config: ApiConfig = ApiConfig.from_env()
    setup_logging()
    app = FastAPI(
        title='Fortu-site',
        version='0.1.0',
        default_response_class=ORJSONResponse,
    )

    web_config: WebConfig = WebConfig.from_env()
    setup_ioc_container(app, web_config)
    setup_middlewares(app, api_config)
    setup_static(app, web_config)
    setup_exception_handlers(app)
    setup_template_routers(app)
    setup_api_routers(app)
    return app


def setup_middlewares(app: FastAPI, api_config: ApiConfig):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_config.cors_origins,
        allow_credentials=True,
        allow_methods=api_config.allow_methods,
        allow_headers=api_config.allow_headers,
    )
    app.add_middleware(TimingMiddleware)


def setup_ioc_container(app: FastAPI, web_config: WebConfig):
    container: AsyncContainer = make_async_container(
        ConfigProvider(),
        SecurityProvider(),
        DatabaseProvider(),
        UseCaseProvider(),
        RepositoriesProvider(),
        context={
            # config
            DatabaseConfig: DatabaseConfig.from_env(),
            AuthConfig: AuthConfig.from_env(),
            # templates
            Jinja2Templates: get_templates(web_config),
        },
    )

    setup_dishka(container, app)


def get_templates(web_config: WebConfig) -> Jinja2Templates:
    templates = Jinja2Templates(directory=web_config.templates_dir)
    return templates


def setup_static(app: FastAPI, web_config: WebConfig):
    app.mount(
        web_config.static_path,
        StaticFiles(directory=web_config.static_dir),
        name='static',
    )
