from fastapi import APIRouter, Request
from app.config.templating import render


router = APIRouter()

@router.get('/')
def index(request: Request):
    return render(request, 'seeder/index.html.j2')