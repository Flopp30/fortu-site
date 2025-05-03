from sqlalchemy import select, desc

from teawish.application.news.interfaces import INewsRepository, NewsListFilter
from teawish.application.news.models import News
from teawish.infrastructure.db.repositories.base import SqlAlchemyBaseRepository


class SqlAlchemyNewsRepository(SqlAlchemyBaseRepository, INewsRepository):
    async def get_news(self, list_filter: NewsListFilter | None = None) -> list[News]:
        where_conditions: list[bool] = []
        if list_filter:
            where_conditions.extend(getattr(News, k) == v for k, v in list_filter.filter_dict.items())
        stmt = select(News).where(*where_conditions).order_by(desc(News.created_at))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
