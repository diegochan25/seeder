from datetime import timedelta
from app import services
from app.core.consts import PYSESSID
from app.core.utils import utcnow
from app.models.session import Session
from app.models.user import User
from fastapi import Response
from sqlalchemy import UUID, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


PYSESSID_COOKIE_ARGS = {
    'key': PYSESSID,
    'path': '/',
    'domain': None,
    'secure': True,
    'httponly': True,
    'samesite': 'lax'
}

async def find_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def find_valid_session(db: AsyncSession, pysessid: str) -> Session | None:
    stmt = (
        select(Session)
        .options(selectinload(Session.user))
        .where(Session.pysessid == pysessid)
        .where(Session.revoked_at.is_(None))
        .where(Session.expires_at > utcnow())
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_session(
    db: AsyncSession, 
    user_id: UUID, 
    max_age: timedelta,
    ip_address: str | None = None, 
    user_agent: str | None = None
) -> str:
    pysessid = services.crypto.randbase64url(32)
    session = Session(
        pysessid = pysessid,
        user_id = user_id,
        ip_address = ip_address,
        user_agent = user_agent,
        expires_at = utcnow() + max_age
    )
    db.add(session)
    await db.flush()
    return pysessid

def set_session_cookie(response: Response, pysessid: str, max_age: timedelta) -> Response:
    response.set_cookie(**PYSESSID_COOKIE_ARGS, value=pysessid, max_age=int(max_age.total_seconds()))
    return response

async def revoke_session(db: AsyncSession, pysessid: str):
    stmt = update(Session).where(Session.pysessid == pysessid).values(revoked_at=utcnow(), expires_at=utcnow() - timedelta(hours=1))
    await db.execute(stmt)
    await db.flush()

def delete_session_cookie(response: Response) -> Response:
    response.delete_cookie(**PYSESSID_COOKIE_ARGS)
    return response