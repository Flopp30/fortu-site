import datetime
from io import BytesIO
from uuid import UUID
import logging
import dataclasses as dc
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Form, UploadFile, File
from fastapi.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from teawish.application.auth.interfaces import ISessionRepository, SessionStorageFilter
from teawish.application.auth.models import Session
from teawish.application.db import IUoW
from teawish.application.launcher.dto import LauncherIn
from teawish.application.launcher.interfaces import ILauncherRepository, ILauncherFileStorage
from teawish.application.launcher.models import Launcher
from teawish.application.launcher.usecases import AdminCreateLauncherUseCase
from teawish.application.news.interfaces import INewsRepository, NewsGetFilter
from teawish.application.news.models import News
from teawish.application.user.exceptions import UserDoesNotExistsException
from teawish.application.user.interfaces import IUserRepository
from teawish.application.user.models import User
from teawish.web.responses import refresh_page_content_response, optional_template_response

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
    session_repo: FromDishka[ISessionRepository],
    templates: FromDishka[Jinja2Templates],
) -> HTMLResponse:
    # FIXME вынести в use case?
    context: dict = {'request': request, 'list_limit': DEFAULT_LIST_LIMIT, 'list_offset': DEFAULT_LIST_OFFSET}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)

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
    user_repo: FromDishka[IUserRepository],
    session_repo: FromDishka[ISessionRepository],
    templates: FromDishka[Jinja2Templates],
    limit: int = DEFAULT_LIST_LIMIT,
    offset: int = DEFAULT_LIST_OFFSET,
) -> HTMLResponse:
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    users: list[User] = await user_repo.get_list(limit, offset)
    total_count: int = await user_repo.total_count()
    context.update(
        {
            'objects': users,
            'total_count': total_count,
            'list_limit': limit,
            'list_offset': offset,
        }
    )
    return templates.TemplateResponse('admin/components/users/list.html', context=context)


@inject
async def launchers_list(
    request: Request,
    launcher_repo: FromDishka[ILauncherRepository],
    session_repo: FromDishka[ISessionRepository],
    templates: FromDishka[Jinja2Templates],
    limit: int = DEFAULT_LIST_LIMIT,
    offset: int = DEFAULT_LIST_OFFSET,
) -> HTMLResponse:
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    launchers: list[Launcher] = await launcher_repo.get_list(limit, offset)
    total_count: int = await launcher_repo.total_count()
    context.update(
        {
            'objects': launchers,
            'total_count': total_count,
            'list_limit': limit,
            'list_offset': offset,
        }
    )
    return templates.TemplateResponse('admin/components/launchers/list.html', context=context)


@inject
async def launchers_form(
    request: Request,
    launcher_repo: FromDishka[ILauncherRepository],
    session_repo: FromDishka[ISessionRepository],
    templates: FromDishka[Jinja2Templates],
    launcher_id: int | None = None,
) -> HTMLResponse:
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    if launcher_id:
        launcher: Launcher = await launcher_repo.get(launcher_id)
        context['object'] = launcher
    return templates.TemplateResponse('admin/components/launchers/form.html', context=context)


@inject
async def launchers_create(
    request: Request,
    templates: FromDishka[Jinja2Templates],
    use_case: FromDishka[AdminCreateLauncherUseCase],
    file: UploadFile = File(...),
    version: str = Form(...),
) -> HTMLResponse:
    context: dict = {'request': request}
    session_id = request.cookies.get('sessionId')
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
    templates: FromDishka[Jinja2Templates],
    session_repo: FromDishka[ISessionRepository],
    launcher_repo: FromDishka[ILauncherRepository],
    file_storage: FromDishka[ILauncherFileStorage],
    version: str,
    file: UploadFile | None = None,
) -> HTMLResponse:
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    # launcher: Launcher = await launcher_repo.get(launcher_id)
    # file_bytes: BytesIO = file_storage.load(launcher.file_path)
    # fixme доделать
    return templates.TemplateResponse('admin/components/launchers/form.html', context=context)


@inject
async def news_list(
    request: Request,
    news_repo: FromDishka[INewsRepository],
    session_repo: FromDishka[ISessionRepository],
    templates: FromDishka[Jinja2Templates],
    limit: int = DEFAULT_LIST_LIMIT,
    offset: int = DEFAULT_LIST_OFFSET,
) -> HTMLResponse:
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    news: list[News] = await news_repo.get_list(limit, offset)
    total_count: int = await news_repo.total_count()
    context.update(
        {
            'objects': news,
            'total_count': total_count,
            'list_limit': limit,
            'list_offset': offset,
        }
    )
    return templates.TemplateResponse('admin/components/news/list.html', context=context)


@inject
async def news_form(
    request: Request,
    session_repo: FromDishka[ISessionRepository],
    news_repo: FromDishka[INewsRepository],
    templates: FromDishka[Jinja2Templates],
    news_id: int | None = None,
) -> HTMLResponse:
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    if news_id:
        context['object'] = await news_repo.get(get_filter=NewsGetFilter(id=news_id))
    return templates.TemplateResponse('admin/components/news/form.html', context=context)


@inject
async def news_create(
    request: Request,
    session_repo: FromDishka[ISessionRepository],
    news_repo: FromDishka[INewsRepository],
    uow: FromDishka[IUoW],
    templates: FromDishka[Jinja2Templates],
    title: str = Form(...),
    text: str = Form(...),
) -> HTMLResponse:
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    news: News = News(title=title, text=text, created_at=datetime.datetime.now(), creator_id=user.id)
    context['object'] = await news_repo.create(news)
    await uow.commit()
    return templates.TemplateResponse('admin/components/news/form.html', context=context)


@inject
async def news_update(
    news_id: int,
    request: Request,
    session_repo: FromDishka[ISessionRepository],
    news_repo: FromDishka[INewsRepository],
    uow: FromDishka[IUoW],
    templates: FromDishka[Jinja2Templates],
    title: str = Form(...),
    text: str = Form(...),
    created_at: str = Form(...),
) -> HTMLResponse:
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    news: News = News(
        title=title, text=text, created_at=datetime.datetime.strptime(created_at, '%H:%M %d.%m.%Y'), creator_id=user.id
    )
    news.id = news_id
    context['object'] = news
    await news_repo.update(news)
    await uow.commit()
    return templates.TemplateResponse('admin/components/news/form.html', context=context)


@inject
async def sessions_list(
    request: Request,
    session_repo: FromDishka[ISessionRepository],
    templates: FromDishka[Jinja2Templates],
    limit: int = DEFAULT_LIST_LIMIT,
    offset: int = DEFAULT_LIST_OFFSET,
):
    context: dict = {'request': request}
    user: User | None = await get_admin_user(request, session_repo)
    if not user:
        return refresh_page_content_response(templates=templates, context=context)
    sessions: list[Session] = await session_repo.get_list(limit=limit, offset=offset)
    total_count: int = await session_repo.total_count()
    context.update(
        {
            'objects': sessions,
            'total_count': total_count,
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
