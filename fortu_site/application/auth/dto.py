import dataclasses as dc

from fortu_site.application.auth.models import Session
from fortu_site.application.user.dto import UserOut


@dc.dataclass
class AuthorizedUser:
    user: UserOut
    session: Session
