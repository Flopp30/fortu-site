from sqlalchemy import select, desc
from sqlalchemy.sql.functions import count

from teawish.application.launcher.exception import LauncherDoesNotExistsException
from teawish.application.launcher.interfaces import ILauncherRepository
from teawish.application.launcher.models import Launcher
from teawish.application.user.models import User
from teawish.infrastructure.db.repositories.base import SqlAlchemyBaseRepository


class SqlAlchemyLauncherRepository(SqlAlchemyBaseRepository, ILauncherRepository):
    async def get(self, launcher_id: int) -> Launcher:
        stmt = select(Launcher).where(Launcher.id == launcher_id)
        res = await self.session.execute(stmt)
        launcher: Launcher | None = res.scalars().one_or_none()
        if launcher is None:
            raise LauncherDoesNotExistsException
        return launcher

    async def get_current(self) -> Launcher:
        stmt = select(Launcher).order_by(desc(Launcher.id)).limit(1)
        res = await self.session.execute(stmt)
        launcher: Launcher | None = res.scalars().one_or_none()
        if launcher is None:
            raise LauncherDoesNotExistsException
        return launcher

    async def create(self, launcher: Launcher) -> Launcher:
        self.session.add(launcher)
        return launcher

    async def get_list(self, limit: int | None = None, offset: int | None = None) -> list[Launcher]:
        stmt = select(Launcher).join(User).order_by(desc(Launcher.created_at))
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def total_count(self) -> int:
        stmt = select(count(Launcher.id)).select_from(Launcher)
        res = await self.session.execute(stmt)
        return res.scalars().first()
