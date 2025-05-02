from functools import partial

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates


def exception_500_template_handler(request: Request, exc: Exception, templates: Jinja2Templates):
    return templates.TemplateResponse('components/500.html', {'request': request}, status_code=500)


def exception_404_template_handler(request: Request, exc: Exception, templates: Jinja2Templates):
    return templates.TemplateResponse('404.html', {'request': request}, status_code=404)


def setup_exception_handlers(app: FastAPI, templates: Jinja2Templates):
    app.add_exception_handler(500, partial(exception_500_template_handler, templates=templates))
    app.add_exception_handler(404, partial(exception_404_template_handler, templates=templates))
