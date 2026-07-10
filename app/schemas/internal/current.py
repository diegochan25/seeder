from pydantic import BaseModel
from app.schemas.internal.session import Session
from app.schemas.internal.user import User

class Current(BaseModel):
    session: Session 
    user: User
