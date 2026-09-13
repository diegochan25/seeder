from types import SimpleNamespace
import uuid
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from app.services import password


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String)

    @property
    def password(self) -> str:
        return SimpleNamespace(
            matches = lambda pw: password.verify(pw, self.password_hash)
        )

    @password.setter
    def password(self, value: str):
        self.password_hash = password.hash(value)