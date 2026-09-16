from datetime import datetime
from pathlib import Path
from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from app.core.consts import FLASH
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


env.globals.update({
    'layout': layout,
    'macro': macro,
    'partial': partial,
    'now': datetime.now
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