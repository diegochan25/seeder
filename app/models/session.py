from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import UUID, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Model


if TYPE_CHECKING:
    from app.models.user import User

class Session(Model):
    pysessid_hash: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    ip_address: Mapped[str | None] = mapped_column(String(length=40))
    user_agent: Mapped[str | None] = mapped_column(String(255))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    data: Mapped[dict] = mapped_column(JSONB, default=dict)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='sessions')

    @property
    def pysessid(self):
        from app import services

        class PysessidComparator:
            @staticmethod
            def matches(sessidstr: str) -> bool:
                return services.crypto.sha256compare(sessidstr, self.pysessid_hash)
        return PysessidComparator

    @pysessid.setter
    def pysessid(self, value: str):
        from app import services
        self.pysessid_hash = services.crypto.sha256hash(value)