from fastapi import FastAPI
from fortu_site.web.template_routers import index


def setup_template_routers(app: FastAPI):
    app.include_router(index.setup())
