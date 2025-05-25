from sqlalchemy import select, desc
from sqlalchemy.sql.functions import count

from teawish.application.installer.exceptions import InstallerDoesNotExistsException
from teawish.application.installer.interfaces import IInstallerRepository
from teawish.application.installer.models import Installer
from teawish.application.user.models import User
from teawish.infrastructure.db.repositories.base import SqlAlchemyBaseRepository


class SqlAlchemyInstallerRepository(SqlAlchemyBaseRepository, IInstallerRepository):
    async def get(self, installer_id: int) -> Installer:
        stmt = select(Installer).where(Installer.id == installer_id)
        res = await self.session.execute(stmt)
        installer: Installer | None = res.scalars().one_or_none()
        if installer is None:
            raise InstallerDoesNotExistsException
        return installer

    async def get_current(self) -> Installer:
        stmt = select(Installer).order_by(desc(Installer.id)).limit(1)
        res = await self.session.execute(stmt)
        installer: Installer | None = res.scalars().one_or_none()
        if installer is None:
            raise InstallerDoesNotExistsException
        return installer

    async def create(self, launcher: Installer) -> Installer:
        self.session.add(launcher)
        return launcher

    async def get_list(self, limit: int | None = None, offset: int | None = None) -> list[Installer]:
        stmt = select(Installer).join(User).order_by(desc(Installer.created_at))
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def total_count(self) -> int:
        stmt = select(count(Installer.id)).select_from(Installer)
        res = await self.session.execute(stmt)
        return res.scalars().first()  # type: ignore
