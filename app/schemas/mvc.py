from typing import Self
from pydantic import BaseModel

class CreateUser(BaseModel):
    email: str
    password: str
    confirm_password: str

    @classmethod
    def empty(cls) -> Self:
        return cls(email='', password='', confirm_password='')

class AuthUser(BaseModel):
    email: str
    password: str
    remember_me: bool = False

    @classmethod
    def empty(cls) -> Self:
        return cls(email='', password='', remember_me=False)

class CreateSchema(BaseModel):
    name: str
    description: str | None = None

    @property
    def schema_name(self) -> str:
        return self.name.replace(' ', '_')


    @classmethod
    def empty(cls) -> Self:
        return cls(name='', description=None)
    