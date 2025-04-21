from datetime import timezone
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Security
from fastapi.responses import ORJSONResponse
from fastapi.security import APIKeyCookie

from fortu_site.application.auth.dto import AuthorizedUser
from fortu_site.application.auth.use_cases import UserRegisterUseCase, UserLoginUseCase, UserLogoutUseCase
from fortu_site.application.user.dto import UserOut
from fortu_site.web.responses import SimpleResponse

session_auth = APIKeyCookie(name='sessionId')


def set_session_cookie_response(auth_user: AuthorizedUser, response: ORJSONResponse) -> UserOut:
    session = auth_user.session
    assert session.id is not None
    assert session.expires_at is not None
    response.set_cookie(
        key='sessionId', value=session.id.hex, httponly=True, expires=session.expires_at.astimezone(timezone.utc)
    )
    return auth_user.user


@inject
async def register(
    email: str,
    password: str,
    name: str,
    response: ORJSONResponse,
    use_case: FromDishka[UserRegisterUseCase],
) -> UserOut:
    auth_user: AuthorizedUser = await use_case(email=email, password=password, name=name)
    return set_session_cookie_response(auth_user, response)


@inject
async def login(
    email: str,
    password: str,
    response: ORJSONResponse,
    use_case: FromDishka[UserLoginUseCase],
) -> UserOut:
    auth_user: AuthorizedUser = await use_case(email=email, password=password)
    return set_session_cookie_response(auth_user, response)


@inject
async def logout(
    response: ORJSONResponse,
    use_case: FromDishka[UserLogoutUseCase],
    session_id: str = Security(session_auth),
) -> SimpleResponse:
    await use_case(session_id=UUID(session_id))
    response.delete_cookie('sessionId', httponly=True)
    return SimpleResponse()


def setup() -> APIRouter:
    router = APIRouter(tags=['auth'])

    router.add_api_route('/register', register, methods=['POST'], description='User registration')

    router.add_api_route('/login', login, methods=['POST'], description='User login')

    router.add_api_route('/logout', logout, methods=['POST'], description='User logout')

    return router
