import dataclasses as dc

from teawish.application.auth.models import Session
from teawish.application.user.dto import UserOut


@dc.dataclass
class AuthorizedUser:
    user: UserOut
    session: Session
