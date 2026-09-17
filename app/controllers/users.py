from fastapi import APIRouter, Request


router = APIRouter(prefix='/users')

@router.patch('/{autoid}')
def update():
    pass