from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from app import services
from app.schemas.internal import flash

def handle_unauthorized(request: Request, exc: Exception):
    if not request.url.path.startswith('/api/'):
        response = RedirectResponse('/auth/login', status_code=303)
        return services.flash.send(flash(type='error', message='Please log in to continue.'), response)
    return JSONResponse(401, detail='Unauthorized.')