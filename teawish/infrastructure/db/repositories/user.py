from collections.abc import Sequence

from sqlalchemy import select, desc
from sqlalchemy.sql.functions import count

from teawish.application.user.exceptions import (
    UserDoesNotExistsException,
    MultipleUserReturnsException,
)
from teawish.application.user.interfaces import IUserRepository, UserStorageFilter
from teawish.application.user.models import User
from teawish.infrastructure.db.repositories.base import SqlAlchemyBaseRepository


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

    async def get_list(self, limit: int | None = None, offset: int | None = None) -> list[User]:
        stmt = select(User).order_by(desc(User.created_at))
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def total_count(self) -> int:
        stmt = select(count(User.id)).select_from(User)
        res = await self.session.execute(stmt)
        return res.scalars().first()
