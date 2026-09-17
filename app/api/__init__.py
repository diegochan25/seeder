from fastapi import APIRouter
from app.api import v1

router = APIRouter(prefix='/api')


@router.get('/health')
def health():
    return { 'status_code': 200, 'message': 'API is reachable.' }

@router.get('/ready')
def ready():
    return { 'status_code': 501, 'message': 'This route has not been implemented.' }


router.include_router(v1.router)