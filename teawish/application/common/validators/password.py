from teawish.application.auth.exceptions import PasswordPolicyViolationException
from teawish.application.common.validators.base import BaseValidator

MIN_PASSWORD_LENGTH: int = 4
MAX_PASSWORD_LENGTH: int = 32
PASSWORD_DIGIT_REQUIRED: bool = True
PASSWORD_LETTER_REQUIRED: bool = True


class RawPasswordValidator(BaseValidator[str]):
    def _validate(self):
        violations: list[str] = []
        if len(self.value) < MIN_PASSWORD_LENGTH:
            violations.append('Too short password')

        if len(self.value) > MAX_PASSWORD_LENGTH:
            violations.append('Too long password')

        if PASSWORD_DIGIT_REQUIRED and not any(char.isdigit() for char in self.value):
            violations.append('Password must contains at least one digit')

        if PASSWORD_LETTER_REQUIRED and not any(char.isalpha() for char in self.value):
            violations.append('Password must contain at least one letter')

        if violations:
            raise PasswordPolicyViolationException('\n'.join(violations))
