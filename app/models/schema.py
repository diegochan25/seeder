import posixpath as path
from slugify import slugify
from sqlalchemy import Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Model


class Schema(Model):
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    index: Mapped[int] = mapped_column(Integer)

    @property
    def slug(self) -> str:
        if self.index > 0:
            return slugify(f"{self.name}-{self.index}")
        return slugify(self.name)

    @property
    def path(self) -> str:
        return path.join(self.autoid, self.slug)


class Field(Model):
    name: Mapped[str] = mapped_column(String, index=True)
    type: Mapped[str] = mapped_column(String)
    generator: Mapped[str] = mapped_column(String)
    options: Mapped[dict] = mapped_column(JSONB, default=dict)