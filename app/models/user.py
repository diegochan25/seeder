from enum import Enum, StrEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Model
from app.services import password

class AccountStatus(StrEnum):
    Unverified = 'unverified'
    Active = 'active'
    Deleted = 'deleted'

class AccountRole(StrEnum):
    User = 'user'
    Staff = 'staff'
    Admin = 'admin'

class User(Model):
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.Unverified)
    role: Mapped[AccountRole] = mapped_column(Enum(AccountRole), default=AccountRole.User)

    @property
    def password(self):
        class PasswordMatches:
            @staticmethod
            def matches(pw: str) -> bool:
                return password.verify(pw, self.password_hash)
        return PasswordMatches

    @password.setter
    def password(self, value: str):
        self.password_hash = password.hash(value)
