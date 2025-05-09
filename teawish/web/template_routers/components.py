from enum import Enum
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from teawish.application.auth.exceptions import ExpiredSessionException
from teawish.application.auth.interfaces import SessionStorageFilter, ISessionRepository
from teawish.application.news.dto import UserNewsOut
from teawish.application.news.use_cases import GetUserNewsUseCase
from teawish.application.user.models import User
from teawish.web.responses import change_browser_location_response, refresh_page_content_response


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
    context: dict = {
        'request': request,
        'user': user,
    }
    response: HTMLResponse = templates.TemplateResponse('components/home.html', context)
    return change_browser_location_response(response, '/')


@inject
async def refresh_page_content(
    request: Request,
    templates: FromDishka[Jinja2Templates],
    session_repo: FromDishka[ISessionRepository],
) -> HTMLResponse:
    user: User | None = None
    session_id = request.cookies.get('sessionId')
    if session_id:
        user = await session_repo.get_user(SessionStorageFilter(session_id=UUID(session_id)))
    context: dict = {
        'request': request,
        'user': user,
    }
    response: HTMLResponse = templates.TemplateResponse('components/refresh_page_content.html', context)
    return change_browser_location_response(response, '/')


class ServerStatus(Enum):
    online = 'online'
    offline = 'offline'


@inject
async def online_indicator(
    request: Request,
    templates: FromDishka[Jinja2Templates],
) -> HTMLResponse:
    context: dict = {
        'request': request,
        'online_users': 1,
        'total_users': 20,
        # 'server_status': ServerStatus.offline.value,
        'server_status': ServerStatus.online.value,
    }
    return templates.TemplateResponse('components/online_indicator.html', context=context)


@inject
async def get_news(
    request: Request,
    templates: FromDishka[Jinja2Templates],
    use_case: FromDishka[GetUserNewsUseCase],
):
    context = {'request': request}
    session_id = request.cookies.get('sessionId')
    if not session_id:
        return refresh_page_content_response(templates, context)

    try:
        # сессия устарела
        news_list: list[UserNewsOut] = await use_case(UUID(session_id))
    except ExpiredSessionException:
        return refresh_page_content_response(templates, context)

    context.update({'news_list': news_list})
    return templates.TemplateResponse('components/news_list.html', context)


def setup() -> APIRouter:
    router = APIRouter(tags=['components'], include_in_schema=False, prefix='/components')
    router.add_api_route('/home', home_page, methods=['GET'])
    router.add_api_route('/refresh_page_content', refresh_page_content, methods=['GET'])
    router.add_api_route('/online_indicator', online_indicator, methods=['GET'])
    router.add_api_route('/news/list', get_news, methods=['GET'])
    return router
