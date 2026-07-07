from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_tailwind import tailwind
from contextlib import asynccontextmanager

base_dir = Path(__file__).resolve().parent
static_dir = base_dir / 'static'


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
