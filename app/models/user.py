from enum import StrEnum
from typing import TYPE_CHECKING
from sqlalchemy import String, Enum
from sqlalchemy.ext.hybrid import hybrid_property
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
    _email: Mapped[str] = mapped_column('email', String(255), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.Unverified)
    role: Mapped[AccountRoles] = mapped_column(Enum(AccountRoles), default=AccountRoles.User)
    _first_name: Mapped[str | None] = mapped_column('first_name', String(255))
    _last_name: Mapped[str | None] = mapped_column('last_name', String(255))

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

    @hybrid_property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> str:
        self._email = value.strip().lower()

    @hybrid_property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> str:
        self._first_name = value.strip()

    @hybrid_property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> str:
        self._last_name = value.strip()