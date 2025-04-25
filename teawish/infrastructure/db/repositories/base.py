import abc

from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyBaseRepository(abc.ABC):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
