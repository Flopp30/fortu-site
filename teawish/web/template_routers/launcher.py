from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse

from teawish.application.launcher.models import Launcher
from teawish.application.launcher.usecases import GetCurrentLauncherUseCase


@inject
async def download_launcher(
    use_case: FromDishka[GetCurrentLauncherUseCase],
):
    launcher: Launcher | None = await use_case()
    if launcher is None:
        raise HTTPException(status_code=404, detail='Файл не найден')
    return FileResponse(
        path=launcher.file_path, filename=launcher.file_path.split('/')[-1], media_type='application/octet-stream'
    )


def setup() -> APIRouter:
    router = APIRouter(tags=['launcher'], include_in_schema=False)
    router.add_api_route('/launcher/download', download_launcher, methods=['GET'])
    return router
