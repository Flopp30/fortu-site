from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from teawish.application.installer.models import Installer
from teawish.application.installer.use_cases import GetCurrentInstallerUseCase
from teawish.web.responses import streaming_file_response
import logging

log = logging.getLogger(__name__)


@inject
async def download_installer(
    use_case: FromDishka[GetCurrentInstallerUseCase],
) -> StreamingResponse:
    installer: Installer | None = await use_case()
    log.error(f'check path: {installer}')

    if installer is None:
        raise HTTPException(status_code=404, detail='Файл не найден')
    return streaming_file_response(installer.file_path)


def setup() -> APIRouter:
    router = APIRouter(tags=['installer'], include_in_schema=False)
    router.add_api_route('/installer/download', download_installer, methods=['GET'])
    return router
