from fastapi import APIRouter, Request
from app.controllers import schemas
from app.dependencies import RequiresAuth
from app.documents.schema import Schema
from app.documents.schema_field import SchemaField

router = APIRouter(prefix='/fields')


@router.post('/')
def new(request: Request, seed_slug: str, schema_slug: str, current: RequiresAuth):
    schema = Schema.find_by(slug=schema_slug)

    field = SchemaField(
        schema_id=schema._id
    ).save()

    pass


schemas.router.include_router(router, prefix='/{schema_slug}')
