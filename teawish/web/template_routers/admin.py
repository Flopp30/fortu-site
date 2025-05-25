import logging
from io import BytesIO
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.params import Security
from fastapi.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from teawish.application.admin.common.use_cases import GetAdminPageUseCase
from teawish.application.admin.installer.use_cases import (
    AdminCreateInstallerUseCase,
    AdminInstallerFormUseCase,
    AdminInstallerListUseCase,
    AdminUpdateInstallerUseCase,
)
from teawish.application.admin.launcher.use_cases import (
    AdminCreateLauncherUseCase,
    AdminLauncherFormUseCase,
    AdminLauncherListUseCase,
    AdminUpdateLauncherUseCase,
)
from teawish.application.admin.news.use_cases import (
    AdminCreateNewsUseCase,
    AdminNewsFormUseCase,
    AdminNewsListUseCase,
    AdminUpdateNewsUseCase,
)
from teawish.application.admin.session.use_cases import AdminSessionListUseCase
from teawish.application.admin.user.use_cases import AdminUsersListUseCase
from teawish.application.installer.dto import InstallerIn
from teawish.application.launcher.dto import LauncherIn
from teawish.web.api_key import TemplateAPIKeyCookie
from teawish.web.responses import optional_template_response, refresh_page_content_response

session_auth = TemplateAPIKeyCookie(name='sessionId')

log = logging.getLogger(__name__)

DEFAULT_LIST_LIMIT: int = 20
DEFAULT_LIST_OFFSET: int = 0


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
    use_case: FromDishka[AdminUsersListUseCase],
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
    use_case: FromDishka[AdminLauncherListUseCase],
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
    use_case: FromDishka[AdminLauncherFormUseCase],
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
    use_case: FromDishka[AdminUpdateLauncherUseCase],
    templates: FromDishka[Jinja2Templates],
    version: str,
    session_id: str = Security(session_auth),
    file: UploadFile | None = None,
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), launcher_id, version)
    context['request'] = request
    # FIXME доделать
    return templates.TemplateResponse('admin/components/launchers/form.html', context=context)


@inject
async def news_list(
    request: Request,
    use_case: FromDishka[AdminNewsListUseCase],
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
    use_case: FromDishka[AdminNewsFormUseCase],
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
    use_case: FromDishka[AdminCreateNewsUseCase],
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
    use_case: FromDishka[AdminUpdateNewsUseCase],
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
    use_case: FromDishka[AdminSessionListUseCase],
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


@inject
async def installers_list(
    request: Request,
    use_case: FromDishka[AdminInstallerListUseCase],
    templates: FromDishka[Jinja2Templates],
    limit: int = DEFAULT_LIST_LIMIT,
    offset: int = DEFAULT_LIST_OFFSET,
    session_id: str = Security(session_auth),
) -> HTMLResponse:
    log.error('heey')
    context: dict = await use_case(UUID(session_id), limit, offset)
    context.update(
        {
            'request': request,
            'list_limit': limit,
            'list_offset': offset,
        }
    )
    return templates.TemplateResponse('admin/components/installers/list.html', context=context)


@inject
async def installers_form(
    request: Request,
    use_case: FromDishka[AdminInstallerFormUseCase],
    templates: FromDishka[Jinja2Templates],
    installer_id: int | None = None,
    session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), installer_id)
    context['request'] = request
    return templates.TemplateResponse('admin/components/installers/form.html', context=context)


@inject
async def installers_create(
    request: Request,
    templates: FromDishka[Jinja2Templates],
    use_case: FromDishka[AdminCreateInstallerUseCase],
    file: UploadFile = File(...),
    version: str = Form(...),
    session_id: str = Security(session_auth),
) -> HTMLResponse:
    context: dict = {'request': request}
    if not session_id:
        return refresh_page_content_response(templates=templates, context=context)
    in_data: InstallerIn = InstallerIn(
        version=version,
        file_name=file.filename,
        file_content=BytesIO(await file.read()),
    )
    context['object'] = await use_case(session_id=UUID(session_id), installer_data=in_data)
    return templates.TemplateResponse('admin/components/installers/form.html', context=context)


@inject
async def installers_update(
    launcher_id: int,
    request: Request,
    use_case: FromDishka[AdminUpdateInstallerUseCase],
    templates: FromDishka[Jinja2Templates],
    version: str,
    session_id: str = Security(session_auth),
    file: UploadFile | None = None,
) -> HTMLResponse:
    context: dict = await use_case(UUID(session_id), launcher_id, version)
    context['request'] = request
    # FIXME доделать
    return templates.TemplateResponse('admin/components/installers/form.html', context=context)


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

    # installers
    router.add_api_route('/installers/list', installers_list, methods=['GET'])
    router.add_api_route('/installers/form', installers_form, methods=['GET'])
    router.add_api_route('/installers/create', installers_create, methods=['POST'])
    router.add_api_route('/installers/update/{installer_id}', installers_update, methods=['POST'])

    # news
    router.add_api_route('/news/list', news_list, methods=['GET'])
    router.add_api_route('/news/form', news_form, methods=['GET'])
    router.add_api_route('/news/create', news_create, methods=['POST'])
    router.add_api_route('/news/update/{news_id}', news_update, methods=['POST'])

    # sessions
    router.add_api_route('/session/list', sessions_list, methods=['GET'])

    return router
