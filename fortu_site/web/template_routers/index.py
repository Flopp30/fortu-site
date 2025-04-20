from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from starlette.templating import Jinja2Templates


@inject
async def index(
    request: Request,
    templates: FromDishka[Jinja2Templates],
) -> HTMLResponse:
    context: dict = {'request': request}
    return templates.TemplateResponse('index.html', context)


def setup() -> APIRouter:
    router = APIRouter(tags=['templates'], include_in_schema=False)
    router.add_api_route('/', index, methods=['GET'])
    return router
