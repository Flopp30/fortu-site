import datetime

from teawish.application.auth.dto import AuthorizedUser
from teawish.application.auth.exceptions import SessionDoesNotExistException, EmailPolicyViolationException, \
    PasswordPolicyViolationException, NamePolicyViolationException, RegistrationValidError, PasswordMismatchException
from teawish.application.auth.interfaces import (
    IPasswordEncryptor,
    ISessionRepository,
    SessionStorageFilter,
    IAuthSessionService,
)
from teawish.application.auth.models import Session, SESSION_ID
from teawish.application.common.validators.email import EmailValidator
from teawish.application.common.validators.name import UserNameValidator
from teawish.application.common.validators.password import RawPasswordValidator
from teawish.application.db import IUoW
from teawish.application.user.dto import UserOut
from teawish.application.user.interfaces import IUserRepository, UserStorageFilter
from teawish.application.user.models import User


class UserRegisterUseCase:
    def __init__(
            self,
            user_repository: IUserRepository,
            session_repository: ISessionRepository,
            uow: IUoW,
            password_encryptor: IPasswordEncryptor,
            session_service: IAuthSessionService,
    ):
        self._user_repository = user_repository
        self._uow = uow
        self._password_encryptor = password_encryptor
        self._session_repository = session_repository
        self._session_service = session_service

    def _validate(self, name: str, email: str, password: str, confirm_password: str):
        errors = {}

        if password != confirm_password:
            errors['confirm_password_errors'] = ["Пароли не совпадают"]

        try:
            EmailValidator(email)
        except EmailPolicyViolationException as e:
            errors['email_errors'] = [str(e)]
        try:
            RawPasswordValidator(password)
        except PasswordPolicyViolationException as e:
            errors['password_errors'] = e.errors
        try:
            UserNameValidator(name)
        except NamePolicyViolationException as e:
            errors['name_errors'] = [str(e)]

        if errors:
            raise RegistrationValidError(errors)

    async def __call__(self, name: str, email: str, password: str, confirm_password: str) -> AuthorizedUser:
        self._validate(name, email, password, confirm_password)
        hashed_pass: str = self._password_encryptor.hash_password(password)

        user: User = await self._user_repository.create(
            User(name=name, email=email, password=hashed_pass, created_at=datetime.datetime.now())
        )
        await self._uow.flush()

        session: Session = self._session_service.create_session(user)
        session = await self._session_repository.create(session)
        await self._uow.commit()

        user_out = UserOut(
            id=user.id, name=user.name, email=user.email, created_at=user.created_at, is_admin=user.is_admin
        )
        return AuthorizedUser(user=user_out, session=session)


class UserLoginUseCase:
    def __init__(
            self,
            user_repository: IUserRepository,
            session_repository: ISessionRepository,
            uow: IUoW,
            password_encryptor: IPasswordEncryptor,
            session_service: IAuthSessionService,
    ):
        self._user_repository = user_repository
        self._uow = uow
        self._password_encryptor = password_encryptor
        self._session_repository = session_repository
        self._session_service = session_service

    async def __call__(self, email: str, password: str) -> AuthorizedUser:
        user: User = await self._user_repository.get(user_filter=UserStorageFilter(email=email))
        is_verify: bool = self._password_encryptor.verify_password(password, user.password)
        if not is_verify:
            raise PasswordMismatchException

        user_out = UserOut(
            id=user.id, name=user.name, email=user.email, created_at=user.created_at, is_admin=user.is_admin
        )
        try:
            session: Session = await self._session_repository.get(get_filter=SessionStorageFilter(user_id=user.id))
        except SessionDoesNotExistException:
            session = self._session_service.create_session(user)
            session = await self._session_repository.create(session)

        await self._uow.commit()
        return AuthorizedUser(user=user_out, session=session)


class UserLogoutUseCase:
    def __init__(
            self,
            session_repository: ISessionRepository,
            uow: IUoW,
    ):
        self._uow = uow
        self._session_repository = session_repository

    async def __call__(self, session_id: SESSION_ID):
        await self._session_repository.revoke(session_id)
        await self._uow.commit()
