from collections.abc import AsyncIterable

from asyncpg import Connection
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from teawish.application.auth.interfaces import ISessionRepository
from teawish.application.db import IUoW
from teawish.application.installer.interfaces import IInstallerRepository
from teawish.application.launcher.interfaces import ILauncherRepository
from teawish.application.news.interfaces import INewsRepository
from teawish.application.user.interfaces import IUserRepository
from teawish.config import DatabaseConfig
from teawish.infrastructure.db.repositories.auth import SqlAlchemySessionRepository
from teawish.infrastructure.db.repositories.installer import SqlAlchemyInstallerRepository
from teawish.infrastructure.db.repositories.launcher import SqlAlchemyLauncherRepository
from teawish.infrastructure.db.repositories.news import SqlAlchemyNewsRepository
from teawish.infrastructure.db.repositories.user import SqlAlchemyUserRepository
from teawish.infrastructure.db.uow import UoW


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, db_config: DatabaseConfig) -> AsyncIterable[AsyncEngine]:
        cache_size: int = db_config.cache_size
        engine = create_async_engine(
            url=f'{db_config.full_url}',
            echo=db_config.echo,
            echo_pool=db_config.echo,
            pool_size=db_config.pool_size,
            connect_args={
                'statement_cache_size': cache_size,
                'connection_class': Connection,
            },
        )
        yield engine
        await engine.dispose(True)

    @provide
    def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_factory() as session:
            yield session

    uow = provide(source=UoW, provides=IUoW, scope=Scope.REQUEST)


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    user = provide(SqlAlchemyUserRepository, provides=IUserRepository)
    session = provide(SqlAlchemySessionRepository, provides=ISessionRepository)
    news = provide(SqlAlchemyNewsRepository, provides=INewsRepository)
    launcher = provide(SqlAlchemyLauncherRepository, provides=ILauncherRepository)
    installer = provide(SqlAlchemyInstallerRepository, provides=IInstallerRepository)
