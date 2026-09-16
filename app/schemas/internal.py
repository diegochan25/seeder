from typing import Literal, Self

from pydantic import BaseModel, Field

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