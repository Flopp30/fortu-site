from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi import Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from teawish.application.auth.dto import AuthorizedUser
from teawish.application.auth.exceptions import RegistrationValidError, PasswordMismatchException
from teawish.application.auth.use_cases import UserRegisterUseCase, UserLogoutUseCase, UserLoginUseCase
from teawish.application.user.exceptions import UserDoesNotExistsException
from teawish.web.responses import success_auth_response, template_target_response


@inject
async def login_form(
        request: Request,
        templates: FromDishka[Jinja2Templates],
) -> HTMLResponse:
    return templates.TemplateResponse('components/login_form.html', {'request': request})


@inject
async def login(
        templates: FromDishka[Jinja2Templates],
        use_case: FromDishka[UserLoginUseCase],
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
) -> HTMLResponse:
    try:
        auth_user: AuthorizedUser = await use_case(email=email, password=password)
    except (UserDoesNotExistsException, PasswordMismatchException) as e:
        context: dict = {'request': request, 'error_message': 'Неверный логин или пароль'}

        response = templates.TemplateResponse(
            "components/login_form.html",
            context
        )
        return template_target_response(response, '#form-container')

    return success_auth_response(auth_user=auth_user, templates=templates, request=request)


@inject
async def register_form(
        request: Request,
        templates: FromDishka[Jinja2Templates],
) -> HTMLResponse:
    return templates.TemplateResponse('components/register_form.html', {'request': request})


@inject
async def register(
        use_case: FromDishka[UserRegisterUseCase],
        templates: FromDishka[Jinja2Templates],
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
        username: str = Form(...),
) -> HTMLResponse:
    try:
        auth_user: AuthorizedUser = await use_case(
            email=email, password=password, confirm_password=confirm_password, name=username
        )
    except RegistrationValidError as e:
        form_data = await request.form()
        context: dict = {'request': request, 'errors': e.args[0]} | dict(form_data)

        response = templates.TemplateResponse(
            "components/register_form.html",
            context
        )

        return template_target_response(response, '#form-container')

    return success_auth_response(auth_user=auth_user, templates=templates, request=request)


@inject
async def logout(
        request: Request,
        use_case: FromDishka[UserLogoutUseCase],
        templates: FromDishka[Jinja2Templates],
):
    session_id: str | None = request.cookies.get('sessionId', None)
    if session_id:
        await use_case(session_id=UUID(session_id))

    response = templates.TemplateResponse('components/refresh_page_content.html', {'request': request})
    response.delete_cookie('sessionId', httponly=True)
    return response


def setup() -> APIRouter:
    router = APIRouter(tags=['templates'], include_in_schema=False, prefix='/templates/auth')
    router.add_api_route('/login', login_form, methods=['GET'])
    router.add_api_route('/login', login, methods=['POST'])
    router.add_api_route('/register', register_form, methods=['GET'])
    router.add_api_route('/register', register, methods=['POST'])
    router.add_api_route('/logout', logout, methods=['POST'])
    return router
