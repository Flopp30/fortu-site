import os

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse

from teawish.config import LauncherConfig


@inject
async def download_launcher(
    config: FromDishka[LauncherConfig],
):
    file_path: str = config.launcher_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='Файл не найден')
    file_name = file_path.split('/')[-1]
    return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')


def setup() -> APIRouter:
    router = APIRouter(tags=['launcher'], include_in_schema=False)
    router.add_api_route('/launcher/download', download_launcher, methods=['GET'])
    return router
