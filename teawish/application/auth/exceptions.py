class EmailPolicyViolationException(Exception): ...


class PasswordPolicyViolationException(Exception):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors


class NamePolicyViolationException(Exception): ...


class SessionDoesNotExistException(Exception): ...


class ExpiredSessionException(Exception): ...


class SessionAlreadyExistsException(Exception): ...


class PasswordMismatchException(Exception): ...


class OperationNotPermittedException(Exception): ...


class FormError(Exception):
    @property
    def has_errors(self) -> bool:
        return any(vars(self).values())

    def to_dict(self) -> dict[str, list[str]]:
        return {error_type: errors for error_type, errors in vars(self).items() if len(errors) > 0}


class RegistrationValidError(FormError):
    def __init__(self) -> None:
        self.password_errors: list[str] = []
        self.confirm_password_errors: list[str] = []
        self.email_errors: list[str] = []
        self.name_errors: list[str] = []


class LoginValidError(FormError):
    def __init__(self) -> None:
        self.password_errors: list[str] = []
        self.email_errors: list[str] = []
