from typing import Annotated

from fastapi import APIRouter, Form, Request
from app.config.templating import render
from app.dependencies import RequiresDB
from app.schemas.mvc import CreateSchema
from app import services

router = APIRouter(prefix='/schemas')

@router.post('/')
async def create(db: RequiresDB, request: Request, data: Annotated[CreateSchema, Form()]):
    result = await services.schemas.create(db, '', data.schema_name, data.description)