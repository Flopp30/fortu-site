from teawish.application.auth.exceptions import ExpiredSessionException
from teawish.application.auth.interfaces import ISessionRepository, SessionStorageFilter
from teawish.application.auth.models import SESSION_ID
from teawish.application.news.dto import UserNewsOut
from teawish.application.news.interfaces import INewsRepository
from teawish.application.news.models import News
from teawish.application.user.exceptions import UserDoesNotExistsException


class GetUserNewsUseCase:
    def __init__(
        self,
        news_repository: INewsRepository,
        session_repository: ISessionRepository,
    ):
        self._news_repository = news_repository
        self._session_repository = session_repository

    async def __call__(self, session_id: SESSION_ID):
        try:
            await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))
        except UserDoesNotExistsException:
            raise ExpiredSessionException('session expired')

        news: list[News] = await self._news_repository.get_news()

        return [UserNewsOut(text=n.text, title=n.title, id=n.id, created_at=n.created_at) for n in news]
