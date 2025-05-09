from functools import partial
from tkinter.font import names

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from teawish.application.auth.exceptions import ExpiredSessionException
from teawish.application.user.exceptions import UserDoesNotExistsException
from teawish.web.responses import change_browser_location_response
from teawish.web.utils import is_htmx_request


def exception_500_template_handler(request: Request, exc: Exception, templates: Jinja2Templates):
    template_location: str = '500.html'
    if is_htmx_request(request):
        template_location = 'components/500_content.html'
    return templates.TemplateResponse(template_location, {'request': request}, status_code=500)


def exception_user_not_found_template_handler(request: Request, exc: Exception, templates: Jinja2Templates):
    if not is_htmx_request(request):
        return RedirectResponse('/')

    response: HTMLResponse = templates.TemplateResponse('components/refresh_page_content.html', {'request': request}, status_code=302)
    response.headers['HX-Retarget'] = '#main-content'
    return change_browser_location_response(response, '/')


def exception_404_template_handler(request: Request, exc: Exception, templates: Jinja2Templates):
    template_location: str = '404.html'
    if is_htmx_request(request):
        template_location = 'components/404_content.html'
    return templates.TemplateResponse(template_location, {'request': request}, status_code=404)


def setup_exception_handlers(app: FastAPI, templates: Jinja2Templates):
    app.add_exception_handler(500, partial(exception_500_template_handler, templates=templates))
    app.add_exception_handler(404, partial(exception_404_template_handler, templates=templates))
    app.add_exception_handler(403, partial(exception_user_not_found_template_handler, templates=templates))
    app.add_exception_handler(UserDoesNotExistsException, partial(exception_user_not_found_template_handler, templates=templates))
    app.add_exception_handler(ExpiredSessionException, partial(exception_user_not_found_template_handler, templates=templates))

