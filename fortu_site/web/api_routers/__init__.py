from fastapi import FastAPI
from fortu_site.web.api_routers import healthcheck


def setup_api_routers(app: FastAPI):
    app.include_router(healthcheck.setup())
