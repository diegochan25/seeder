from fastapi import APIRouter, Request
from app.config.templates import templates
from app.documents.seed import Seed
router = APIRouter(prefix='/seeds')

@router.get('/')
def index(request: Request):
    seeds = Seed.list()
    return templates.TemplateResponse(
        request, 
        'seeds/index.html.j2', 
        context={
            'seeds': seeds
        }
    )
    

@router.get('/new')
def new(request:  Request):
    seeds = Seed.list()
    return templates.TemplateResponse(
        request, 
        'seeds/new.html.j2', 
        context={
            'seeds': seeds
        }
    )
