import dataclasses as dc
import logging
from datetime import datetime
from uuid import UUID

from dishka import FromDishka

from teawish.application.admin.exceptions import AccessDenied
from teawish.application.auth.interfaces import (
    ISessionRepository,
    SessionStorageFilter,
)
from teawish.application.db import IUoW
from teawish.application.news.interfaces import INewsRepository, NewsGetFilter
from teawish.application.news.models import News
from teawish.application.user.interfaces import IUserRepository
from teawish.application.user.models import User

log = logging.getLogger(__name__)


class AdminNewsListUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        session_repository: ISessionRepository,
        news_repo: FromDishka[INewsRepository],
    ):
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._news_repo = news_repo

    async def __call__(self, session_id: UUID, limit: int, offset: int) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        news: list[News] = await self._news_repo.get_list(limit, offset)
        total_count: int = await self._news_repo.total_count()

        context = {
            'objects': news,
            'total_count': total_count,
            'list_limit': limit,
            'list_offset': offset,
        }
        return context


class AdminNewsFormUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
        news_repo: INewsRepository,
    ):
        self._session_repository = session_repository
        self._news_repo = news_repo

    async def __call__(self, session_id: UUID, news_id: int) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        context = {}
        if news_id:
            context['object'] = await self._news_repo.get(get_filter=NewsGetFilter(id=news_id))

        return context


class AdminCreateNewsUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
        news_repo: INewsRepository,
        uow: IUoW,
    ):
        self._session_repository = session_repository
        self._news_repo = news_repo
        self._uow = uow

    async def __call__(self, session_id: UUID, title: str, text: str) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        news: News = News(title=title, text=text, created_at=datetime.now(), creator_id=user.id)
        context: dict = {'object': await self._news_repo.create(news)}

        await self._uow.commit()
        return context


class AdminUpdateNewsUseCase:
    def __init__(
        self,
        session_repository: ISessionRepository,
        news_repo: INewsRepository,
        uow: IUoW,
    ):
        self._session_repository = session_repository
        self._news_repo = news_repo
        self._uow = uow

    async def __call__(self, session_id: UUID, news_id, title: str, text: str, created_at: str) -> dict:
        user: User = await self._session_repository.get_user(SessionStorageFilter(session_id=session_id))

        if not user.is_admin:
            log.warning(f'Trying to open admin page without permissions: {dc.asdict(user)}')
            raise AccessDenied

        news: News = News(
            id=news_id,
            title=title,
            text=text,
            created_at=datetime.strptime(created_at, '%H:%M %d.%m.%Y'),
            creator_id=user.id,
        )
        context = {'object': news}
        await self._news_repo.update(news)
        await self._uow.commit()

        return context
