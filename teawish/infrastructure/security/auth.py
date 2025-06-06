import datetime

from teawish.application.auth.exceptions import ExpiredSessionException
from teawish.application.auth.interfaces import IAuthSessionService
from teawish.application.auth.models import Session
from teawish.application.user.models import User
from teawish.config import AuthConfig


class AuthSessionService(IAuthSessionService):
    def __init__(self, auth_config: AuthConfig):
        self.session_ttl_sec: int = auth_config.session_ttl_sec

    def get_expires_at(self) -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(seconds=self.session_ttl_sec)

    def check_session(self, session: Session):
        expired_at: datetime.datetime | None = session.expired_at
        if expired_at is None or expired_at < self.get_expires_at():
            raise ExpiredSessionException

    def create_session(self, user: User) -> Session:
        return Session(
            user_id=user.id,
            created_at=datetime.datetime.now(),
            expired_at=self.get_expires_at(),
        )
