import re

from teawish.application.auth.exceptions import NamePolicyViolationException
from teawish.application.common.validators.base import BaseValidator

MAX_NAME_LENGTH: int = 16
MIN_NAME_LENGTH: int = 3
NAME_PATTERN: re.Pattern = re.compile(r'[A-Za-z0-9_]+')


class UserNameValidator(BaseValidator[str]):
    def _validate(self):
        if len(self.value) > MAX_NAME_LENGTH:
            raise NamePolicyViolationException('Слишком длинное имя')

        if len(self.value) < MIN_NAME_LENGTH:
            raise NamePolicyViolationException('Слишком короткое имя')

        if not NAME_PATTERN.match(self.value):
            raise NamePolicyViolationException(f'Недопустимый формат имени: {self.value}')
