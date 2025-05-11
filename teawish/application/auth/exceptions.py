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


class RegistrationValidError(ValueError): ...
