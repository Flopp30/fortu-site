import dataclasses as dc
from typing import Literal

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dc.dataclass
class HealthcheckResult:
    status: Literal['ok', 'error']
    text: str | None = None


@inject
async def healthcheck(session: FromDishka[AsyncSession]):
    code: int = 200
    content: dict = {'status': 'ok'}
    try:
        await session.execute(text('SELECT 1'))
    except ConnectionRefusedError:
        code = 500
        content = {'status': 'error', 'text': 'db connection error'}
    except Exception as e:
        code = 500
        content = {'status': 'error', 'text': str(e)}
    return ORJSONResponse(status_code=code, content=content)


def setup() -> APIRouter:
    router = APIRouter(tags=['tech'])
    router.add_api_route(
        '/healthcheck',
        healthcheck,
        methods=['GET'],
        description='Simple healthcheck router',
        response_model=HealthcheckResult,
    )

    return router
