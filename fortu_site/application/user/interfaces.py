import dataclasses as dc
from types import EllipsisType
from typing import Protocol

from fortu_site.application.common.filters.base import BaseEllipsisFilter
from fortu_site.application.user.models import User


@dc.dataclass
class UserStorageFilter(BaseEllipsisFilter):
    email: str | None | EllipsisType = ...
    id: int | None | EllipsisType = ...


class IUserRepository(Protocol):
    async def create(self, user: User) -> User: ...

    async def get(self, user_filter: UserStorageFilter) -> User: ...
