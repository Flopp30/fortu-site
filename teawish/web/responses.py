import dataclasses as dc

from datetime import timezone

from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from teawish.application.auth.dto import AuthorizedUser


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
