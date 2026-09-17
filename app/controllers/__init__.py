from fastapi import APIRouter, Depends, Request
from app.config.templating import render
from app.controllers import auth, schemas
from app.dependencies import load_schemas, RequiresSession, verify_csrf_token
from app.schemas.mvc import CreateSchema

router = APIRouter(dependencies=[Depends(load_schemas), Depends(verify_csrf_token)])

@router.get('/')
async def index(request: Request, session: RequiresSession):
    return render(request, 'views/index.html.j2', new_schema=CreateSchema.empty())

router.include_router(auth.router)
router.include_router(schemas.router)