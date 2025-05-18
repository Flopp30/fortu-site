from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from teawish.application.news.use_cases import NonAuthorizedUserNews


@inject
async def get_news(
        use_case: FromDishka[NonAuthorizedUserNews],
):
    return await use_case()


def setup() -> APIRouter:
    router = APIRouter(tags=['news'])
    router.add_api_route('/api/news/list', get_news, methods=['GET'])
    return router
