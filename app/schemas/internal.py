from typing import Literal, Self
from pydantic import BaseModel, Field
from sqlalchemy import UUID
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
    email: str
    role: str

    @classmethod
    def from_user(cls, user: User) -> SessionUser:
        return cls(id=user.id, email=user.email, role=str(user.role))

class Session(BaseModel):
    user: SessionUser
    ip_address: str | None
    user_agent: str | None
    data: dict

    @property
    def user_id(self) -> UUID:
        return self.user.id


    @classmethod
    def from_session(cls, session: InternalSession) -> InternalSession:
        return cls(user=SessionUser.from_user(session.user), data=session.data)