from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.config.templates import templates
from app.controllers import seeds
from app.dependencies import RequiresAuth, FromForm
from app.documents.schema import Schema
from app.documents.seed import Seed
from app.schemas.request.create_schema import CreateSchema


router = APIRouter(prefix='/schemas')

@router.get('/new')
def new(request: Request, seed_slug: str, current: RequiresAuth):
    seed = Seed.find_by(slug=seed_slug, user_id=ObjectId(current.user.id))
    schemas = Schema.list_by(seed_id=seed._id)
    return templates.TemplateResponse(
        request,
        'schemas/new.html.j2',
        context={
            'seed': seed,
            'schemas': schemas
        }
    )


@router.get('/{slug}')
def show(request: Request, seed_slug: str, slug: str, current: RequiresAuth):
    seed = Seed.find_by(slug=seed_slug, user_id=ObjectId(current.user.id))
    schemas = Schema.list_by(seed_id=seed._id)
    schema = Schema.find_by(slug=slug, seed_id=seed._id)
    return templates.TemplateResponse(
        request,
        'schemas/show.html.j2',
        context={
            'seed': seed,
            'schemas': schemas,
            'schema': schema
        }
    )

@router.post('/')
def create(seed_slug: str, data: FromForm[CreateSchema], current: RequiresAuth):
    seed = Seed.find_by(slug=seed_slug, user_id=ObjectId(current.user.id))
    if not seed:
        raise HTTPException(403, 'Forbidden.')
    
    slug, index = Schema.next_slug_and_index_for(data.name)

    schema = Schema(
        seed_id=seed._id,
        name=data.name,
        index=index,
        slug=slug
    ).save()

    if schema:
        return RedirectResponse(f"/seeds/{seed_slug}/schemas/{schema.slug}/", status_code=302)


@router.patch('/{slug}')
def update(request: Request, seed_slug: str, current: RequiresAuth):
    pass


seeds.router.include_router(router, prefix='/{seed_slug}')