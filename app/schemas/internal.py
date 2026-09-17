from typing import Literal, Self
from pydantic import BaseModel, Field
from uuid import UUID
from app.models.user import User
from app.models.session import Session as InternalSession

class FlashMessage(BaseModel):
    type: Literal['info', 'success', 'warning', 'error'] = 'info'
    message: str = ''

    @classmethod
    def parse(cls, jsonstr: str) -> Self:
        return cls.model_validate_json(jsonstr)

    def stringify(self) -> str:
        return self.model_dump_json()

flash = FlashMessage
    
class ClientInfo(BaseModel):
    ip_address: str | None
    user_agent: str | None
    

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit  

class SessionUser(BaseModel):
    id: UUID
    autoid: int
    email: str
    role: str
    first_name: str | None = None
    last_name: str | None = None

    @classmethod
    def from_user(cls, user: User) -> SessionUser:
        return cls(
            id=user.id,
            autoid=user.autoid,
            email=user.email,
            role=str(user.role), 
            first_name=user.first_name, 
            last_name=user.last_name
        )

    @property
    def full_name(self) -> str:
        if not self.first_name: # Do not use only last name
            return ''
        full = self.first_name
        if self.last_name:
            full += ' ' + self.last_name
        return full

    @property
    def username(self) -> str:
        if self.full_name:
            return self.full_name
        else:
            return self.email

class Session(BaseModel):
    user: SessionUser
    ip_address: str | None = None
    user_agent: str | None = None
    data: dict

    @property
    def user_id(self) -> UUID:
        return self.user.id


    @classmethod
    def from_session(cls, session: InternalSession) -> InternalSession:
        return cls(
            user=SessionUser.from_user(session.user), 
            data=session.data,
            ip_address=session.ip_address,
            user_agent=session.user_agent
        )