import re

from fortu_site.application.auth.exceptions import NamePolicyViolationException
from fortu_site.application.common.validators.base import BaseValidator

MAX_NAME_LENGTH: int = 32
MIN_NAME_LENGTH: int = 4
NAME_PATTERN: re.Pattern = re.compile(r'[A-Za-zА-Яа-яЕё]+')


class UserNameValidator(BaseValidator[str]):
    def _validate(self):
        if len(self.value) > MAX_NAME_LENGTH:
            raise NamePolicyViolationException('Too long user name')

        if len(self.value) < MIN_NAME_LENGTH:
            raise NamePolicyViolationException('Too short user name')

        if not NAME_PATTERN.match(self.value):
            raise NamePolicyViolationException(f'Wrong user name format: {self.value}')
