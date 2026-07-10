from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_tailwind import tailwind
from app.controllers import auth, schemas, seeds

dirname = Path(__file__).resolve().parent
static_dir = dirname / 'static'


@asynccontextmanager
async def lifespan(_: FastAPI):
    process = tailwind.compile(
        str(static_dir / 'css' / 'output.css'),
        tailwind_stylesheet_path=str(static_dir / 'css' / 'input.css'),
    )
    yield
    process.terminate()


app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory=static_dir), name='static')

app.include_router(auth.router)
app.include_router(seeds.router)

@app.get('/')
def index():
    raise HTTPException(301, headers={ 'location': '/seeds/' })

@app.exception_handler(HTTPException)
async def send_to_login(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse('/auth/login/', status_code=303)
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def redirect_on_validation_error(request: Request, _: RequestValidationError):
    referer = request.headers.get('referer', '/')
    return RedirectResponse(referer, status_code=303)
