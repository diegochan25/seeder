from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_tailwind import tailwind
from app.controllers import seeds

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

app.include_router(seeds.router)

@app.get('/')
def index():
    raise HTTPException(301, headers={ 'location': '/seeds/' })
