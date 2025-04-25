from collections.abc import Sequence

from sqlalchemy import Select, select, text, Update, update

from teawish.application.auth.exceptions import SessionAlreadyExistsException, SessionDoesNotExistException
from teawish.application.auth.interfaces import ISessionRepository, SessionStorageFilter
from teawish.application.auth.models import Session, SESSION_ID
from teawish.application.user.exceptions import UserDoesNotExistsException
from teawish.application.user.models import User
from teawish.infrastructure.db.repositories.base import SqlAlchemyBaseRepository


class SqlAlchemySessionRepository(SqlAlchemyBaseRepository, ISessionRepository):
    async def create(self, session: Session) -> Session:
        try:
            await self.get(get_filter=SessionStorageFilter(user_id=session.user_id))
            raise SessionAlreadyExistsException
        except SessionDoesNotExistException:
            pass
        self.session.add(session)
        return session

    async def get_user(self, get_filter: SessionStorageFilter) -> User:
        subquery: Select = select(Session).where(
            Session.id == get_filter.session_id,
            Session.expired_at >= text("'now()'"),
        )
        stmt: Select = select(User).where(
            User.id == subquery.c.user_id,
        )
        res = await self.session.execute(stmt)
        users: Sequence[User] = res.scalars().all()

        if not users:
            raise UserDoesNotExistsException('User does not exists')

        return users[0]

    async def get(self, get_filter: SessionStorageFilter) -> Session:
        where_condition = [getattr(Session, k) == v for k, v in get_filter.filter_dict.items()]
        stmt: Select = select(Session).where(
            *where_condition,
            Session.expired_at >= text("'now()'"),
        )
        res = await self.session.execute(stmt)
        sessions: Sequence[Session] = res.scalars().all()
        if not sessions:
            raise SessionDoesNotExistException('Session does not exists')
        return sessions[0]

    async def revoke(self, session_id: SESSION_ID):
        stmt: Update = (
            update(Session)
            .where(
                Session.id == session_id,
            )
            .values(
                expired_at=text("'now()'"),
            )
        )
        await self.session.execute(stmt)
