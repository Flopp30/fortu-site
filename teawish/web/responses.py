import dataclasses as dc
from datetime import timezone

from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from teawish.application.auth.dto import AuthorizedUser
from teawish.web.utils import is_htmx_request


@dc.dataclass
class SimpleResponse:
    message: str = 'OK'


def success_auth_response(auth_user: AuthorizedUser, request: Request, templates: Jinja2Templates) -> HTMLResponse:
    session = auth_user.session
    user = auth_user.user
    assert session.id is not None
    assert session.expired_at is not None
    response = templates.TemplateResponse('components/refresh_page_content.html', {'request': request, 'user': user})
    response.set_cookie(
        key='sessionId',
        value=session.id.hex,
        httponly=True,
        path='/',
        expires=session.expired_at.astimezone(timezone.utc),
    )
    return response


def change_browser_location_response(response: HTMLResponse, new_location: str) -> HTMLResponse:
    response.headers['HX-Replace-Url'] = new_location
    return response


def refresh_page_content_response(templates: Jinja2Templates, context: dict) -> HTMLResponse:
    response = templates.TemplateResponse('components/refresh_page_content.html', context)
    response.headers['HX-Retarget'] = '#main-content'
    return change_browser_location_response(response, '/')


def optional_template_response(
        request: Request,
        templates: Jinja2Templates,
        base_template: str,
        htmx_template: str,
        context: dict,
        new_location: str | None = None,
) -> HTMLResponse:
    """В зависимости от типа запроса подставляет разные шаблоны"""
    template_name: str = base_template
    if is_htmx_request(request):
        template_name = htmx_template
    response = templates.TemplateResponse(template_name, context=context)
    if new_location is not None:
        return change_browser_location_response(response, new_location)
    return response


def template_target_response(response: HTMLResponse, target: str) -> HTMLResponse:
    response.headers['HX-Retarget'] = target
    return response
