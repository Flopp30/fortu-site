import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from teawish.application.launcher.models import Launcher
from teawish.application.launcher.use_cases import GetCurrentLauncherUseCase
from teawish.web.responses import streaming_file_response

log = logging.getLogger(__name__)


@inject
async def download_launcher(
    use_case: FromDishka[GetCurrentLauncherUseCase],
) -> StreamingResponse:
    launcher: Launcher | None = await use_case()
    if launcher is None:
        raise HTTPException(status_code=404, detail='Файл не найден')
    return streaming_file_response(launcher.file_path)


def setup() -> APIRouter:
    router = APIRouter(tags=['launcher'], include_in_schema=False)
    router.add_api_route('/launcher/download', download_launcher, methods=['GET'])
    return router
