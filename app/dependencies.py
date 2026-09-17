import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app import services
from app.config.db import engine
from app.config.settings import Settings, get_settings
from app.core.consts import PYSESSID
from app.schemas.internal import ClientInfo, PaginationParams, Session as SessionSchema

logger = logging.getLogger(__name__)

settings = get_settings()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSession(engine) as session:
            yield session
            await session.commit()
    except SQLAlchemyError as e:
        logger.exception(e)
        await session.rollback()
        raise RuntimeError('An error occurred during a database session.') from e


get_session_context = asynccontextmanager(get_session)


async def get_client_info(request: Request):
    if settings.trust_proxy:
        forwarded_for = request.headers.get('x-forwarded-for')
        if forwarded_for:
            ip_address = forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.headers.get('x-real-ip')
    else:
        ip_address = request.client.host if request.client else None

    user_agent = request.headers.get('user-agent')

    return ClientInfo(ip_address=ip_address, user_agent=user_agent)


async def get_pagination(request: Request):
    params = PaginationParams()

    if (page := request.query_params.get('page')):
        params.page = page
    if (limit := request.query_params.get('limit')):
        params.limit = limit
        
    return params


RequiresDB = Annotated[AsyncSession, Depends(get_session)]


async def get_current_session(request: Request, db: RequiresDB) -> SessionSchema:
    pysessid = request.cookies.get(PYSESSID)
    if not pysessid:
        raise HTTPException(401, detail='Not authenticated.')

    session = await services.auth.find_valid_session(db, pysessid)
    if session is None:
        raise HTTPException(401, detail='Not authenticated.')

    return SessionSchema.from_session(session)


RequiresSession = Annotated[SessionSchema, Depends(get_current_session)]

RequiresSettings = Annotated[Settings, Depends(get_settings)]

RequiresClientInfo = Annotated[ClientInfo, Depends(get_client_info)]

RequiresPagination = Annotated[PaginationParams, Depends(get_pagination)]
