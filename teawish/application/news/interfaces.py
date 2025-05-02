import dataclasses as dc
from types import EllipsisType
from typing import Protocol
from collections.abc import Sequence

from teawish.application.common.filters.base import BaseEllipsisFilter
from teawish.application.news.models import News
from teawish.application.user.models import USER_ID


@dc.dataclass
class NewsFilter(BaseEllipsisFilter):
    id: int | None | EllipsisType = ...


class NewsListFilter(NewsFilter):
    creator_id: USER_ID | None | EllipsisType = ...
    limit: int | None | EllipsisType = ...
    offset: int | None | EllipsisType = ...


class NewsRepository(Protocol):
    async def get_news(self, list_filter: NewsListFilter) -> Sequence[News]: ...
