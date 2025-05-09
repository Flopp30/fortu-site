import dataclasses as dc
import logging
from io import BytesIO
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Form, UploadFile, File
from fastapi.params import Security
from fastapi.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from teawish.application.admin.use_cases.admin import GetAdminPageUseCase
from teawish.application.admin.use_cases.launcher import GetLaunchersFormPageUseCase, UpdateLaunchersPageUseCase, GetLaunchersListPageUseCase
from teawish.application.admin.use_cases.news import GetNewsListPageUseCase, GetNewsFormPageUseCase, CreateNewsFormPageUseCase, UpdateNewsPageUseCase
from teawish.application.admin.use_cases.session import GetSessionListPageUseCase
from teawish.application.admin.use_cases.user import GetUsersListPageUseCase
from teawish.application.auth.interfaces import ISessionRepository, SessionStorageFilter
from teawish.application.launcher.dto import LauncherIn
from teawish.application.launcher.use_cases import AdminCreateLauncherUseCase
from teawish.application.user.exceptions import UserDoesNotExistsException
from teawish.application.user.models import User
from teawish.web.api_key import TemplateAPIKeyCookie
from teawish.web.responses import refresh_page_content_response, optional_template_response

session_auth = TemplateAPIKeyCookie(name="sessionId")

log = logging.getLogger(__name__)

DEFAULT_LIST_LIMIT: int = 20
DEFAULT_LIST_OFFSET: int = 0


async def get_admin_user(request: Request, session_repo: ISessionRepository) -> User | None:
    session_id = request.cookies.get('sessionId')
    if not session_id:
        return None
    try:
        user: User = await session_repo.get_user(SessionStorageFilter(session_id=UUID(hex=session_id)))
    except UserDoesNotExistsException:
        return None
    if not user.is_admin:
        log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
        return None
    return user


@inject
async def admin_page(
        request: Request,
        use_case: FromDishka[GetAdminPageUseCase],
        templates: FromDishka[Jinja2Templates],
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = {'request': request, 'list_limit': DEFAULT_LIST_LIMIT, 'list_offset': DEFAULT_LIST_OFFSET}
    user = await use_case(UUID(session_id))

    context['user'] = user
    return optional_template_response(
        request=request,
        templates=templates,
        base_template='admin/admin.html',
        htmx_template='admin/components/admin_content.html',
        context=context,
        new_location='/admin/admin_index',
    )


@inject
async def users_list(
        request: Request,
        use_case: FromDishka[GetUsersListPageUseCase],
        templates: FromDishka[Jinja2Templates],
        limit: int = DEFAULT_LIST_LIMIT,
        offset: int = DEFAULT_LIST_OFFSET,
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), limit, offset)
    context.update(
        {
            'request': request,
            'list_limit': limit,
            'list_offset': offset,
        }
    )
    return templates.TemplateResponse('admin/components/users/list.html', context=context)


@inject
async def launchers_list(
        request: Request,
        use_case: FromDishka[GetLaunchersListPageUseCase],
        templates: FromDishka[Jinja2Templates],
        limit: int = DEFAULT_LIST_LIMIT,
        offset: int = DEFAULT_LIST_OFFSET,
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), limit, offset)
    context.update(
        {
            'request': request,
            'list_limit': limit,
            'list_offset': offset,
        }
    )
    return templates.TemplateResponse('admin/components/launchers/list.html', context=context)


@inject
async def launchers_form(
        request: Request,
        use_case: FromDishka[GetLaunchersFormPageUseCase],
        templates: FromDishka[Jinja2Templates],
        launcher_id: int | None = None,
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), launcher_id)
    context['request'] = request
    return templates.TemplateResponse('admin/components/launchers/form.html', context=context)


@inject
async def launchers_create(
        request: Request,
        templates: FromDishka[Jinja2Templates],
        use_case: FromDishka[AdminCreateLauncherUseCase],
        file: UploadFile = File(...),
        version: str = Form(...),
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = {'request': request}
    if not session_id:
        return refresh_page_content_response(templates=templates, context=context)
    in_data: LauncherIn = LauncherIn(
        version=version,
        file_name=file.filename,
        file_content=BytesIO(await file.read()),
    )
    context['object'] = await use_case(session_id=UUID(session_id), launcher_data=in_data)
    return templates.TemplateResponse('admin/components/launchers/form.html', context=context)


@inject
async def launchers_update(
        launcher_id: int,
        request: Request,
        use_case: FromDishka[UpdateLaunchersPageUseCase],
        templates: FromDishka[Jinja2Templates],
        version: str,
        session_id: str = Security(session_auth),
        file: UploadFile | None = None,
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), launcher_id, version)
    context['request'] = request

    return templates.TemplateResponse('admin/components/launchers/form.html', context=context)


@inject
async def news_list(
        request: Request,
        use_case: FromDishka[GetNewsListPageUseCase],
        templates: FromDishka[Jinja2Templates],
        limit: int = DEFAULT_LIST_LIMIT,
        offset: int = DEFAULT_LIST_OFFSET,
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), limit, offset)
    context['request'] = request

    return templates.TemplateResponse('admin/components/news/list.html', context=context)


@inject
async def news_form(
        request: Request,
        use_case: FromDishka[GetNewsFormPageUseCase],
        templates: FromDishka[Jinja2Templates],
        news_id: int | None = None,
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), news_id)
    context['request'] = request

    return templates.TemplateResponse('admin/components/news/form.html', context=context)


@inject
async def news_create(
        request: Request,
        use_case: FromDishka[CreateNewsFormPageUseCase],
        templates: FromDishka[Jinja2Templates],
        title: str = Form(...),
        text: str = Form(...),
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), title, text)
    context['request'] = request
    return templates.TemplateResponse('admin/components/news/form.html', context=context)


@inject
async def news_update(
        news_id: int,
        request: Request,
        use_case: FromDishka[UpdateNewsPageUseCase],
        templates: FromDishka[Jinja2Templates],
        title: str = Form(...),
        text: str = Form(...),
        created_at: str = Form(...),
        session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), news_id, title, text, created_at)
    context['request'] = request
    return templates.TemplateResponse('admin/components/news/form.html', context=context)


@inject
async def sessions_list(
        request: Request,
        use_case: FromDishka[GetSessionListPageUseCase],
        templates: FromDishka[Jinja2Templates],
        limit: int = DEFAULT_LIST_LIMIT,
        offset: int = DEFAULT_LIST_OFFSET,
        session_id: str = Security(session_auth),
):
    context: dict = await use_case(UUID(session_id), limit, offset)
    context.update(
        {
            'request': request,
            'list_limit': limit,
            'list_offset': offset,
        }
    )
    return templates.TemplateResponse('admin/components/sessions/list.html', context=context)


def setup() -> APIRouter:
    router = APIRouter(tags=['admin'], include_in_schema=False, prefix='/admin')
    router.add_api_route('/admin_index', admin_page, methods=['GET'])

    # users
    router.add_api_route('/users/list', users_list, methods=['GET'])

    # launchers
    router.add_api_route('/launchers/list', launchers_list, methods=['GET'])
    router.add_api_route('/launchers/form', launchers_form, methods=['GET'])
    router.add_api_route('/launchers/create', launchers_create, methods=['POST'])
    router.add_api_route('/launchers/update/{launcher_id}', launchers_update, methods=['POST'])

    # news
    router.add_api_route('/news/list', news_list, methods=['GET'])
    router.add_api_route('/news/form', news_form, methods=['GET'])
    router.add_api_route('/news/create', news_create, methods=['POST'])
    router.add_api_route('/news/update/{news_id}', news_update, methods=['POST'])

    # sessions
    router.add_api_route('/session/list', sessions_list, methods=['GET'])

    return router
