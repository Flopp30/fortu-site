import dataclasses as dc
from types import EllipsisType
from typing import Protocol

from teawish.application.common.filters.base import BaseEllipsisFilter
from teawish.application.user.models import User, USER_ID


@dc.dataclass
class UserStorageFilter(BaseEllipsisFilter):
    email: str | None | EllipsisType = ...
    id: USER_ID | None | EllipsisType = ...


class IUserRepository(Protocol):
    async def create(self, user: User) -> User: ...

    async def get(self, user_filter: UserStorageFilter) -> User: ...
