from datetime import datetime, timezone
from typing import Annotated
from bson import ObjectId
from slugify import slugify
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from app.config.templates import templates
from app.dependencies import RequiresAuth
from app.documents.schema import Schema
from app.documents.seed import Seed
from app.schemas.request.create_seed import CreateSeed
router = APIRouter(prefix='/seeds')

@router.get('/')
def index(request: Request, current: RequiresAuth):
    seed_ids = [s._id for s in Seed.list_by(user_id=current.user.id)]
    schemas = Schema.group_by_seed_ids(seed_ids)
    return templates.TemplateResponse(
        request, 
        'seeds/index.html.j2',
        context={
            'schemas': schemas
        }
    )

@router.get('/{slug}')
def show(request: Request, slug: str, current: RequiresAuth):
    seed = Seed.find_by(slug=slug, user_id=ObjectId(current.user.id))
    schemas = Schema.list_by(seed_id = seed._id)
    return templates.TemplateResponse(
        request, 
        'seeds/show.html.j2',
        context={
            'seed': seed,
            'schemas': schemas
        }
    )

@router.post('/')
def new(data: Annotated[CreateSeed, Form()], current: RequiresAuth):
    max_index = Seed.with_max_index_by_name(data.name)

    index = max_index.index + 1 if max_index else 0
    base_slug = f"{data.name} {index}" if index else data.name

    seed = Seed(
        name=data.name,
        index=index,
        slug=slugify(base_slug),
        description=data.description,
        user_id=current.user.id,
        created_at=datetime.now(timezone.utc)
    ).save()

    schema_max_index = Schema.with_max_index_by_name(data.name)
    schema_index = schema_max_index.index + 1 if schema_max_index else 0
    schema_base_slug = f"{data.schema_name} {index}" if index else data.schema_name

    Schema(
        seed_id=seed._id,
        name=data.schema_name,
        index=schema_index,
        slug=slugify(schema_base_slug)
    ).save()

    return RedirectResponse(url='/seeds/', status_code=302)