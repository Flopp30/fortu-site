from fastapi import FastAPI
from teawish.web.template_routers import index, auth, components, launcher


def setup_template_routers(app: FastAPI):
    routers = [
        index.setup(),
        auth.setup(),
        components.setup(),
        launcher.setup(),
    ]
    for router in routers:
        app.include_router(router)
