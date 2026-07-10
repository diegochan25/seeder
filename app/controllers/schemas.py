from bson import ObjectId
from fastapi import APIRouter, Request
from app.config.templates import templates
from app.controllers import seeds
from app.dependencies import RequiresAuth
from app.documents.schema import Schema
from app.documents.seed import Seed


router = APIRouter(prefix='/schemas')

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

@router.get('/new')
def create(request: Request, seed_slug: str, current: RequiresAuth):
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

@router.post('/')
def new(request: Request, seed_slug: str, current: RequiresAuth):
    pass


@router.patch('/{slug}')
def update(request: Request, seed_slug: str, current: RequiresAuth):
    pass


seeds.router.include_router(router, prefix='/{seed_slug}')