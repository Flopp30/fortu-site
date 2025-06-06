from sqlalchemy.orm import registry, relationship

from teawish.application.auth.models import Session
from teawish.application.installer.models import Installer
from teawish.application.launcher.models import Launcher
from teawish.application.news.models import News
from teawish.application.user.models import User
from teawish.infrastructure.db.tables import (
    installers_table,
    launchers_table,
    metadata,
    news_table,
    sessions_table,
    users_table,
)

mapper_registry = registry(metadata=metadata)

mapper_registry.map_imperatively(
    User,
    users_table,
    properties={
        'sessions': relationship(Session, back_populates='user'),
        'created_news': relationship(News, back_populates='creator'),
        'created_launchers': relationship(Launcher, back_populates='creator'),
        'created_installers': relationship(Installer, back_populates='creator'),
    },
)

mapper_registry.map_imperatively(
    Session,
    sessions_table,
    properties={
        'user': relationship(User, back_populates='sessions'),
    },
)

mapper_registry.map_imperatively(
    News,
    news_table,
    properties={
        'creator': relationship(User, back_populates='created_news', lazy='joined'),
    },
)


mapper_registry.map_imperatively(
    Launcher,
    launchers_table,
    properties={
        'creator': relationship(User, back_populates='created_launchers', lazy='joined'),
    },
)


mapper_registry.map_imperatively(
    Installer,
    installers_table,
    properties={
        'creator': relationship(User, back_populates='created_installers', lazy='joined'),
    },
)
