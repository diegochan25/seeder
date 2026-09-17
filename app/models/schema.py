import posixpath as path
import uuid
from typing import TYPE_CHECKING
from slugify import slugify
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Model

if TYPE_CHECKING:
    from app.models.user import User


class Schema(Model):
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    index: Mapped[int] = mapped_column(Integer)
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='schemas')
    fields: Mapped[list['Field']] = relationship(back_populates='schema')

    @property
    def slug(self) -> str:
        if self.index > 0:
            return slugify(f"{self.name}-{self.index}")
        return slugify(self.name)

    @property
    def path(self) -> str:
        return path.join(str(self.autoid), self.slug)


class Field(Model):
    name: Mapped[str] = mapped_column(String(255), index=True)
    type: Mapped[str] = mapped_column(String(255))
    generator: Mapped[str] = mapped_column(String(255))
    options: Mapped[dict] = mapped_column(JSONB, default=dict)

    schema_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('schemas.id'))
    schema: Mapped[Schema] = relationship(back_populates='fields')