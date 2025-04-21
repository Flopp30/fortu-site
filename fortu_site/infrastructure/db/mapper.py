from sqlalchemy.orm import registry, relationship

from fortu_site.application.auth.models import Session
from fortu_site.application.user.models import User
from fortu_site.infrastructure.db.tables import metadata, users_table, sessions_table

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
