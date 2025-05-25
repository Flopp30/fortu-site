import argparse
import asyncio
import datetime

from asyncpg import Connection
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from teawish.application.user.models import User
from teawish.config.config import DatabaseConfig
from teawish.infrastructure.db.repositories.user import SqlAlchemyUserRepository
from teawish.infrastructure.security.password import PasswordEncryptor


async def create_super_user(username: str, password: str, email: str | None = None):
    db_config = DatabaseConfig.from_env()
    engine: AsyncEngine = create_async_engine(
        url=db_config.full_url,
        echo=db_config.echo,
        echo_pool=db_config.echo,
        pool_size=db_config.pool_size,
        connect_args={
            'connection_class': Connection,
        },
    )

    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        user_repo = SqlAlchemyUserRepository(session=session)
        user: User = User(
            name=username,
            email=email or username,
            created_at=datetime.datetime.now(),
            is_admin=True,
            password=PasswordEncryptor().hash_password(raw_password=password),
        )
        await user_repo.create(user)
        await session.commit()

    print(f'User {username} created with password {password}')


def main():
    parser = argparse.ArgumentParser(description='Создать суперпользователя')
    parser.add_argument('--username', required=True, help='Имя пользователя')
    parser.add_argument('--password', required=True, help='Пароль')
    parser.add_argument('--email', default=None, help='Email (опционально)')

    args = parser.parse_args()

    asyncio.run(create_super_user(args.username, args.password, args.email))


if __name__ == '__main__':
    main()
