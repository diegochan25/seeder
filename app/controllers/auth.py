from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.config.templates import templates
from app.dependencies import RequiresClientInfo, RequiresPasswordService
from app.documents.session import Session
from app.documents.user import User
from app.schemas.request.login_user import LoginUser


router = APIRouter(prefix='/auth')


@router.get('/login')
def login(request: Request):
    return templates.TemplateResponse(request, 'auth/login.html.j2')

@router.post('/login')
def authenticate(data: Annotated[LoginUser, Form()], client_info: RequiresClientInfo, pw_service: RequiresPasswordService):
    unauthorized = HTTPException(401, 'Unauthorized')
    user = User.find_by(email=data.email)
    if not user:
        raise unauthorized
    if not pw_service.compare(user.password_hash, data.password):
        raise unauthorized
    
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=30)

    session = Session(
        uid = user._id,
        ip_address=client_info.ip_address,
        user_agent=client_info.user_agent,
        created_at=now,
        expires_at=exp,
        data={}
    ).save()


    response = RedirectResponse(url='/seeds/', status_code=302)
    response.set_cookie(
        key='pysessid',
        value=str(session._id),
        expires=exp,
        path='/',
        httponly=True,
        secure=True,
        samesite='strict'
    )

    return response
