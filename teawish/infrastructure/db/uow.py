from sqlalchemy.ext.asyncio import AsyncSession

from teawish.application.db import IUoW


class UoW(IUoW):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self):
        await self.session.flush()
