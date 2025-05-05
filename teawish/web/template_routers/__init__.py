from fastapi import FastAPI, APIRouter
from teawish.web.template_routers import index, auth, components, launcher, admin


def setup_template_routers(app: FastAPI):
    routers: list[APIRouter] = [
        index.setup(),
        auth.setup(),
        components.setup(),
        launcher.setup(),
        admin.setup(),
    ]
    for router in routers:
        app.include_router(router)
