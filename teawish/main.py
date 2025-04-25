from fastapi import FastAPI

from teawish.web.main import create_app


app: FastAPI = create_app()
