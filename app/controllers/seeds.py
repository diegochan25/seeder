from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from app.config.templates import templates
from app.dependencies import FromForm, RequiresAuth
from app.documents.schema import Schema
from app.documents.seed import Seed
from app.schemas.request.create_seed import CreateSeed
from app.schemas.request.update_seed import UpdateSeed

router = APIRouter(prefix="/seeds")


@router.get("/")
def index(request: Request, current: RequiresAuth):
    seed_ids = [s._id for s in Seed.list_by(user_id=current.user.id)]
    schemas = Schema.group_by_seed_ids(seed_ids)
    return templates.TemplateResponse(
        request, "seeds/index.html.j2", context={"schemas": schemas}
    )


@router.get("/{slug}")
def show(request: Request, slug: str, current: RequiresAuth):
    seed = Seed.find_by(slug=slug, user_id=ObjectId(current.user.id))
    schemas = Schema.list_by(seed_id=seed._id)
    return templates.TemplateResponse(
        request, "seeds/show.html.j2", context={"seed": seed, "schemas": schemas}
    )


@router.post("/")
def new(data: FromForm[CreateSeed], current: RequiresAuth):
    slug, index = Seed.next_slug_and_index_for(data.name)

    seed = Seed(
        name=data.name,
        index=index,
        slug=slug,
        description=data.description,
        user_id=current.user.id,
        created_at=datetime.now(timezone.utc),
    ).save()

    schema_slug, schema_index = Schema.next_slug_and_index_for(data.schema_name)

    Schema(
        seed_id=seed._id,
        name=data.schema_name,
        index=schema_index,
        slug=schema_slug,
    ).save()

    return RedirectResponse(url="/seeds/", status_code=302)


@router.patch("/{slug}")
def update(slug: str, data: FromForm[UpdateSeed], current: RequiresAuth):
    seed = Seed.find_by(slug=slug, user_id=current.user.id)
    if not seed:
        raise HTTPException(403, 'Forbidden.')
    
    if not data.name == seed.name:
        new_slug, new_index = Seed.next_slug_and_index_for(data.name)
        seed.name = data.name
        seed.slug = new_slug
        seed.index = new_index
    seed.description = data.description
    seed.save()

    return Response(status_code=200, headers={"Location": f"/seeds/{seed.slug}"})