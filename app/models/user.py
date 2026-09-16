from enum import StrEnum
from typing import TYPE_CHECKING
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Model

if TYPE_CHECKING:
    from app.models.schema import Schema
    from app.models.session import Session

class AccountStatus(StrEnum):
    Unverified = 'unverified'
    Active = 'active'
    Deleted = 'deleted'

class AccountRoles(StrEnum):
    User = 'user'
    Staff = 'staff'
    Admin = 'admin'

class User(Model):
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.Unverified)
    role: Mapped[AccountRoles] = mapped_column(Enum(AccountRoles), default=AccountRoles.User)

    schemas: Mapped[list['Schema']] = relationship(back_populates='user')
    sessions: Mapped[list['Session']] = relationship(back_populates='user')

    @property
    def password(self):
        from app.services import password

        class PasswordMatches:
            @staticmethod
            def matches(pw: str) -> bool:
                return password.verify(pw, self.password_hash)
        return PasswordMatches

    @password.setter
    def password(self, value: str):
        from app.services import password
        self.password_hash = password.hash(value)
