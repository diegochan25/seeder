from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from app import services
from app.config.templating import render
from app.controllers import fields
from app.core.generators import GENERATORS
from app.dependencies import RequiresDB, RequiresSession
from app.schemas.internal import flash
from app.schemas.mvc import CreateSchema

router = APIRouter(prefix='/schemas')

@router.get('/')
async def index(request: Request, db: RequiresDB, session: RequiresSession):
    schemas = await services.schemas.own(db, session.user_id)
    return render(request, 'views/schemas/index.html.j2', schemas=schemas)

@router.get('/{autoid}/{_}')
async def show(request: Request, autoid: int, _: str, db: RequiresDB, session: RequiresSession):
    schema = await services.schemas.own_by_autoid(db, session.user_id, autoid)
    if schema is None:
        response = RedirectResponse(f"/schemas/", status_code=303)
        return services.flash.send(flash(type='error', message='That schema could not be found.'), response)
    return render(request, 'views/schemas/show.html.j2', schema=schema, generators=GENERATORS)

@router.post('/')
async def create(data: Annotated[CreateSchema, Form()], db: RequiresDB, session: RequiresSession):
    result = await services.schemas.create(db, session.user_id, data.schema_name, data.description)
    response = RedirectResponse(f"/schemas/{result.autoid}/{result.slug}", status_code=303)
    return services.flash.send(flash(type='success', message='Schema saved successfully!'), response)


router.include_router(fields.router)