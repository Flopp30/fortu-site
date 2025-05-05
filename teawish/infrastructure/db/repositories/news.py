from sqlalchemy import select, desc, update
from sqlalchemy.sql.functions import count

from teawish.application.news.exceptions import NewsDoesNotExists
from teawish.application.news.interfaces import INewsRepository, NewsGetFilter
from teawish.application.news.models import News
from teawish.application.user.models import User
from teawish.infrastructure.db.repositories.base import SqlAlchemyBaseRepository


class SqlAlchemyNewsRepository(SqlAlchemyBaseRepository, INewsRepository):
    async def get_list(self, limit: int | None = None, offset: int | None = None) -> list[News]:
        stmt = select(News).join(User).order_by(desc(News.created_at))
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def total_count(self) -> int:
        stmt = select(count(News.id)).select_from(News)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get(self, get_filter: NewsGetFilter) -> News:
        where_condition = [getattr(News, k) == v for k, v in get_filter.filter_dict.items()]
        stmt = select(News).where(*where_condition)
        res = await self.session.execute(stmt)
        news: News | None = res.scalars().one_or_none()
        if not news:
            raise NewsDoesNotExists
        return news

    async def create(self, news: News) -> News:
        self.session.add(news)
        return news

    async def update(self, news: News):
        stmt = (
            update(News)
            .where(News.id == news.id)
            .values(
                created_at=news.created_at,
                title=news.title,
                text=news.text,
            )
        )
        await self.session.execute(stmt)
