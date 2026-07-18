from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.controllers import schemas
from app.dependencies import RequiresAuth, FromForm
from app.documents.schema import Schema
from app.documents.schema_field import SchemaField
from app.documents.seed import Seed
from app.schemas.request.create_field import CreateField

router = APIRouter(prefix='/fields')


@router.post('/')
def create(request: Request, data: FromForm[CreateField], seed_slug: str, schema_slug: str, current: RequiresAuth):
    schema = Schema.find_by(slug=schema_slug)

    SchemaField(
        schema_id=schema._id,
        name=data.name,
        generator=data.generator,
        generator_label=data.generator_label,
        options=data.options
    ).save()

    return RedirectResponse(f"/seeds/{seed_slug}/schemas/{schema_slug}", 302)

@router.delete('/{id}')
def destroy(id: str, seed_slug: str, schema_slug: str, current: RequiresAuth):
    forbidden = HTTPException(403, 'Forbidden.')
    found = RedirectResponse(f"/seeds/{seed_slug}/schemas/{schema_slug}", 302)

    field = SchemaField.find_by_id(ObjectId(id))

    if not field:
        return found
    
    schema = Schema.find_by_id(field.schema_id)
    if schema is None:
        raise forbidden
    seed = Seed.find_by_id(schema.seed_id)
    if seed is None:
        raise forbidden
    if not current.user.id == seed.user_id:
        raise forbidden
    
    field.delete()
    return found

schemas.router.include_router(router, prefix='/{schema_slug}')
