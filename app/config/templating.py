from datetime import datetime
from pathlib import Path
import secrets
from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, pass_context
from markupsafe import Markup
from app.core.consts import CSRF_TOKEN, FLASH, PYSESSID
from app.schemas.internal import FlashMessage
from app import services

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / 'templates'

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def layout(path: str):  
    return f"layouts/{path}"


def macro(path: str):   
    return f"macros/{path}"


def partial(path: str):
    return f"partials/{path}"

@pass_context
def csrf_token(context: dict) -> Markup:
    request: Request = context['request']
    pysessid = request.cookies.get(PYSESSID)
    if pysessid is None:
        return Markup('')
    token = services.crypto.sha256hmac(pysessid)
    return Markup(f'<input type="hidden" name="{CSRF_TOKEN}" value="{token}">')

env.globals.update({
    'layout': layout,
    'macro': macro,
    'partial': partial,
    'now': datetime.now,
    'csrf_token': csrf_token
})

templates = Jinja2Templates(env=env)

def render(
    request: Request,
    filename: str,
    status_code: int = 200,
    headers: dict[str, str] = {},
    content_type: str | None = None,
    flash: FlashMessage | None = None,
    **context: Any,
):
    from_cookie = flash is None
    if from_cookie:
        flash = services.flash.read(request)
    context.setdefault('schemas', getattr(request.state, 'schemas', []))
    context.setdefault('session', getattr(request.state, 'session', None))
    response = templates.TemplateResponse(
        request,
        filename,
        {
            **context,
            FLASH: flash
        },
        headers=headers,
        status_code=status_code,
        media_type=content_type
    )
    if from_cookie and flash is not None:
        services.flash.clear(response)
    return response