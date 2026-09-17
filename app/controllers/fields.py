from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from app import services
from app.core.generators import GENERATORS
from app.dependencies import RequiresDB, RequiresSession
from app.schemas.internal import flash
from app.schemas.mvc import CreateField

router = APIRouter()

@router.post('/{autoid}/{_}/fields/')
async def create(autoid: int, _: str, data: Annotated[CreateField, Form()], request: Request, db: RequiresDB, session: RequiresSession):
    schema = await services.schemas.own_by_autoid(db, session.user_id, autoid)
    if schema is None:
        response = RedirectResponse('/schemas/', status_code=303)
        return services.flash.send(flash(type='error', message='That schema could not be found.'), response)

    generator = GENERATORS.get(data.generator)
    if generator is None:
        response = RedirectResponse(f"/schemas/{schema.path}", status_code=303)
        return services.flash.send(flash(type='error', message='That generator could not be found.'), response)

    raw = await request.form()
    options = {option.name: option.to_python(raw.get(option.name)) for option in generator.options}

    await services.fields.create(db, schema.id, data.name, generator, options)
    response = RedirectResponse(f"/schemas/{schema.path}", status_code=303)
    return services.flash.send(flash(type='success', message='Field added.'), response)