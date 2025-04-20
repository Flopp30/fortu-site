from fortu_site.application.auth.interfaces import IPasswordEncryptor
from fortu_site.application.db import IUoW
from fortu_site.application.user.dto import UserOut
from fortu_site.application.user.interfaces import IUserRepository, UserStorageFilter
from fortu_site.application.user.models import User
from fortu_site.application.common.validators.email import EmailValidator
from fortu_site.application.common.validators.name import UserNameValidator
from fortu_site.application.common.validators.password import RawPasswordValidator


class UserRegisterUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        uow: IUoW,
        password_encryptor: IPasswordEncryptor,
    ):
        self._user_repository = user_repository
        self._uow = uow
        self._password_encryptor = password_encryptor

    async def __call__(self, name: str, email: str, password: str) -> UserOut:
        EmailValidator(email)
        RawPasswordValidator(password)
        UserNameValidator(name)
        hashed_pass: str = self._password_encryptor.hash_password(password)
        user: User = await self._user_repository.create(User(name=name, email=email, password=hashed_pass))
        await self._uow.commit()
        return UserOut(id=user.id, name=user.name, email=user.email, created_at=user.created_at)


class UserLoginUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        uow: IUoW,
        password_encryptor: IPasswordEncryptor,
    ):
        self._user_repository = user_repository
        self._uow = uow
        self._password_encryptor = password_encryptor

    async def __call__(self, email: str, password: str) -> UserOut:
        EmailValidator(email)
        RawPasswordValidator(password)
        user: User = await self._user_repository.get(user_filter=UserStorageFilter(email=email))
        self._password_encryptor.verify_password(password, user.password)
        # FIXME сессия?
        return UserOut(id=user.id, name=user.name, email=user.email, created_at=user.created_at)


class UserLogoutUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        uow: IUoW,
    ):
        self._user_repository = user_repository
        self._uow = uow

    async def __call__(self):
        # FIXME сессия?
        pass
