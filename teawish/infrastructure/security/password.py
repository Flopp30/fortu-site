import bcrypt

from teawish.application.auth.interfaces import IPasswordEncryptor


class PasswordEncryptor(IPasswordEncryptor):
    def hash_password(self, raw_password: str) -> str:
        hashed_password = bcrypt.hashpw(password=raw_password.encode(), salt=bcrypt.gensalt())
        return hashed_password.decode()

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password=raw_password.encode(), hashed_password=hashed_password.encode())
