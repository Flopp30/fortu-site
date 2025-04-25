from sqlalchemy.orm import registry, relationship

from teawish.application.auth.models import Session
from teawish.application.user.models import User
from teawish.infrastructure.db.tables import metadata, users_table, sessions_table

mapper_registry = registry(metadata=metadata)

mapper_registry.map_imperatively(
    User,
    users_table,
    properties={
        'sessions': relationship(Session, back_populates='user'),
    },
)

mapper_registry.map_imperatively(
    Session,
    sessions_table,
    properties={
        'user': relationship(User, back_populates='sessions'),
    },
)
