import asyncio
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def hash(password: str) -> str:
    return hasher.hash(password)


def verify(password: str, hash: str) -> bool:
    try:
        hasher.verify(hash, password)
        return True
    except VerifyMismatchError:
        return False
