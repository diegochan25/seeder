from typing import Self
from pydantic import BaseModel


class CreateSchema(BaseModel):
    name: str
    description: str | None = None

    @property
    def schema_name(self) -> str:
        return self.name.replace(' ', '_')


    @classmethod
    def empty(cls) -> Self:
        return cls(name='', description=None)
    