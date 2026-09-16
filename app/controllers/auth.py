from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from app import services
from app.config.templating import render
from app.core.consts import LONG_SESSION, SHORT_SESSION
from app.dependencies import RequiresDB, RequiresClientInfo
from app.schemas.internal import FlashMessage
from app.schemas.mvc import AuthUser


router = APIRouter(prefix='/auth')

@router.get('/login')
async def render_login(request: Request):
    login = AuthUser.empty()
    return render(request, 'views/auth/login.html.j2', form=login)

@router.post('/login', status_code=200)
async def auth_user(request: Request, data: Annotated[AuthUser, Form()], db: RequiresDB, client_info: RequiresClientInfo):
    user = await services.auth.find_by_email(db, email=data.email)

    to_login = render(
        request,
        'views/auth/login.html.j2',
        form=data,
        status_code=401,
        flash=FlashMessage(type='error', message='Please check your credentials and try again.'),
    )

    if user is None:
        return to_login

    if not user.password.matches(data.password):
        return to_login

    max_age = LONG_SESSION if data.remember_me else SHORT_SESSION

    pysessid = await services.auth.create_session(
        db,
        user.id,
        max_age,
        client_info.ip_address,
        client_info.user_agent
    )

    response = RedirectResponse('/')
    services.auth.set_session_cookie(response, pysessid, max_age)
    return response