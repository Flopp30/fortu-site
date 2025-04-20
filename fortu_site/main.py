from fastapi import FastAPI

from fortu_site.web.main import create_app


app: FastAPI = create_app()
