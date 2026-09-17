from typing import overload
from fastapi import HTTPException, Request, Response
from pydantic import ValidationError
from app.core.consts import FLASH
from app.schemas.internal import FlashMessage


FLASH_COOKIE_ARGS = {
    'key': FLASH,
    'path': '/',
    'domain': None,
    'secure': True,
    'httponly': True,
    'samesite': 'none'
}

@overload
def send[T: Response](message: FlashMessage, response: T) -> T: ...
@overload
def send(message: FlashMessage, response: None) -> Response: ...
def send[T: Response | None](message: FlashMessage, response: T = None) -> T | Response:
    if response is None:
        response = Response()
    response.set_cookie(**FLASH_COOKIE_ARGS, max_age= 10, value=message.stringify())
    return response

def read(request: Request) -> FlashMessage | None:
    flash = request.cookies.get(FLASH)
    if not flash:
        return None
    try:
        return FlashMessage.parse(flash)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail='services.flash: Flash cookie\'s value is malformed.') from e

def clear(response: Response):
    response.delete_cookie(**FLASH_COOKIE_ARGS)