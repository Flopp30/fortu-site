from fastapi import FastAPI
from fortu_site.web.api_routers import healthcheck, auth


def setup_api_routers(app: FastAPI):
    routers = [
        healthcheck,
        auth,
    ]
    for router in routers:
        app.include_router(router.setup())
