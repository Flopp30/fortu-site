from fastapi import FastAPI
from teawish.web.api_routers import healthcheck, news, auth


def setup_api_routers(app: FastAPI):
    app.include_router(healthcheck.setup())
    app.include_router(news.setup())
    app.include_router(auth.setup())
