from fastapi import FastAPI
from teawish.web.template_routers import index, auth, components


def setup_template_routers(app: FastAPI):
    app.include_router(index.setup())
    app.include_router(auth.setup())
    app.include_router(components.setup())
