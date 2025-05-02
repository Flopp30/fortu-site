from functools import partial

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from teawish.web.utils import is_htmx_request


def exception_500_template_handler(request: Request, exc: Exception, templates: Jinja2Templates):
    template_location: str = '500.html'
    if is_htmx_request(request):
        template_location = 'components/500_content.html'
    return templates.TemplateResponse(template_location, {'request': request}, status_code=500)


def exception_404_template_handler(request: Request, exc: Exception, templates: Jinja2Templates):
    template_location: str = '404.html'
    if is_htmx_request(request):
        template_location = 'components/404_content.html'
    return templates.TemplateResponse(template_location, {'request': request}, status_code=404)


def setup_exception_handlers(app: FastAPI, templates: Jinja2Templates):
    app.add_exception_handler(500, partial(exception_500_template_handler, templates=templates))
    app.add_exception_handler(404, partial(exception_404_template_handler, templates=templates))
