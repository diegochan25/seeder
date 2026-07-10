from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordService:
    hasher = PasswordHasher()

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.hasher.hash(password)
    
    @classmethod
    def compare(cls, hash: str, password: str) -> bool:
        try:
            cls.hasher.verify(hash, password)
            return True
        except (VerifyMismatchError):
            return False
