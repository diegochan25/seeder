from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import UUID, DateTime, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property, Comparator
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.elements import ColumnElement
from app.models.base import Model


if TYPE_CHECKING:
    from app.models.user import User

class PysessIdComparator(Comparator):
    def __eq__(self, other: object) -> ColumnElement[bool]:
        from app import services
        return self.__clause_element__() == services.crypto.sha256hash(other)

    def __clause_element__(self):
        return self.expression

class Session(Model):
    pysessid_hash: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    ip_address: Mapped[str | None] = mapped_column(String(length=40))
    user_agent: Mapped[str | None] = mapped_column(String(255))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    data: Mapped[dict] = mapped_column(JSONB, default=dict)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='sessions')

    @hybrid_property
    def pysessid(self):
        raise AttributeError('Session.pysessid is a write-only property.')
  
    @pysessid.setter
    def pysessid(self, value: str):
        from app import services
        self.pysessid_hash = services.crypto.sha256hash(value)

    @pysessid.comparator
    def pysessid(cls):
        return PysessIdComparator(cls.pysessid_hash)