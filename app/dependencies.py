from datetime import datetime, timezone
from typing import Annotated, TypeVar
from bson import ObjectId
from fastapi import Cookie, Depends, Form, HTTPException, Request

from app.documents.session import Session
from app.documents.user import User
from app.schemas.internal.client_info import ClientInfo
from app.schemas.internal.current import Current
from app.schemas.internal.session import Session as SessionDTO
from app.schemas.internal.user import User as UserDTO
from app.services.password_service import PasswordService


def get_client_info(request: Request) -> ClientInfo:
    ip_address = request.headers.get('x-forwarded-for', request.client.host).split(',')[0].strip()
    user_agent = request.headers.get('user-agent', '<unknown>')
    return ClientInfo(ip_address=ip_address, user_agent=user_agent)

RequiresClientInfo = Annotated[ClientInfo, Depends(get_client_info)]


def get_current_user(request: Request, pysessid: str | None = Cookie(default=None)) -> Current:
    unauthorized = HTTPException(401, 'Unauthorized.')
    if pysessid is None:
        raise unauthorized

    _id = ObjectId(pysessid)

    session = Session.find_by_id(_id)

    if not session:
        raise unauthorized

    if session.expires_at <= datetime.now(timezone.utc):
        session.delete()
        raise unauthorized

    user = User.find_by_id(session.uid)

    if not user:
        raise unauthorized

    current = Current(
        session=SessionDTO(
            _id=session._id,
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            data=session.data
        ),
        user = UserDTO(
            _id=user._id,
            email=user.email
        )
    )

    request.state.current = current

    return current

RequiresAuth = Annotated[Current, Depends(get_current_user)]


def pw_service() -> type[PasswordService]:
    return PasswordService

RequiresPasswordService = Annotated[type[PasswordService], Depends(pw_service)]

T = TypeVar('T')
FromForm = Annotated[T, Form()]