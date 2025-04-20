from collections.abc import Sequence

from sqlalchemy import select

from fortu_site.application.user.exceptions import (
    UserDoesNotExistsException,
    MultipleUserReturnsException,
)
from fortu_site.application.user.interfaces import IUserRepository, UserStorageFilter
from fortu_site.application.user.models import User
from fortu_site.infrastructure.db.repositories.base import SqlAlchemyBaseRepository


class SqlAlchemyUserRepository(SqlAlchemyBaseRepository, IUserRepository):
    async def create(self, user: User) -> User:
        self.session.add(user)
        return user

    async def get(self, user_filter: UserStorageFilter) -> User:
        where_condition = [getattr(User, k) == v for k, v in user_filter.filter_dict.items()]

        stmt = select(User).where(*where_condition)
        res = await self.session.execute(stmt)
        users: Sequence[User] = res.scalars().all()

        if not users:
            raise UserDoesNotExistsException('User does not exists')

        if len(users) > 1:
            raise MultipleUserReturnsException('Multiple user returns')

        return users[0]
