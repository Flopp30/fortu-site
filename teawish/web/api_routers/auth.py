from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, HTTPException

from teawish.application.auth.dto import AuthorizedUser
from teawish.application.auth.exceptions import PasswordMismatchException
from teawish.application.auth.use_cases import UserLoginUseCase
from teawish.application.user.exceptions import UserDoesNotExistsException


@inject
async def login(
        use_case: FromDishka[UserLoginUseCase],
        email: str = Body(...),
        password: str = Body(...),
) -> AuthorizedUser:
    try:
        auth_user: AuthorizedUser = await use_case(email=email, password=password)
        return auth_user
    except (UserDoesNotExistsException, PasswordMismatchException):
        raise HTTPException(400, 'Неверный логин или пароль')


def setup() -> APIRouter:
    router = APIRouter(tags=['auth'])
    router.add_api_route('/api/auth/login', login, methods=['POST'])
    return router
