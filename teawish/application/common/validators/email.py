import re

from teawish.application.auth.exceptions import EmailPolicyViolationException
from teawish.application.common.validators.base import BaseValidator

EMAIL_PATTERN: re.Pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zа-я]{2,}$')


class EmailValidator(BaseValidator[str]):
    def _validate(self):
        if not EMAIL_PATTERN.match(self.value):
            raise EmailPolicyViolationException('Некорректный email')
