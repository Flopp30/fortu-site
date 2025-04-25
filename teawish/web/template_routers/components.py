from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from teawish.application.auth.interfaces import SessionStorageFilter, ISessionRepository
from teawish.application.user.models import User


@inject
async def home_page(
    request: Request,
    templates: FromDishka[Jinja2Templates],
    session_repo: FromDishka[ISessionRepository],
) -> HTMLResponse:
    user: User | None = None
    session_id = request.cookies.get('sessionId')
    if session_id:
        user = await session_repo.get_user(SessionStorageFilter(session_id=UUID(session_id)))
    context: dict = {'request': request, 'user': user}
    return templates.TemplateResponse('components/home.html', context)


def setup() -> APIRouter:
    router = APIRouter(tags=['components'], include_in_schema=False)
    router.add_api_route('/components/home', home_page, methods=['GET'])
    return router
