from fastapi import APIRouter, Request
from app.config.templating import render
from app.controllers import auth, schemas
from app.schemas.mvc import CreateSchema

router = APIRouter()

@router.get('/')
async def index(request: Request):
    return render(request, 'views/index.html.j2', new_schema=CreateSchema.empty())

router.include_router(auth.router)
router.include_router(schemas.router)