from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.consts import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.models.schema import Schema

async def own_highest_index_by_name(db: AsyncSession, owner_id: UUID, name: str) -> int:
    stmt = select(Schema.index).where(Schema.user_id == owner_id, Schema.name == name)
    result = await db.execute(stmt)
    index = result.scalar_one_or_none()
    if index is None:
        return 0
    return index

async def own(db: AsyncSession, owner_id: UUID, limit: int = DEFAULT_PAGE_SIZE, offset: int = 0) -> list[Schema]:
    limit = min(limit, MAX_PAGE_SIZE)
    offset = max(offset, 0)
    stmt = select(Schema).where(Schema.user_id == owner_id).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def own_by_autoid(db: AsyncSession, owner_id: UUID, autoid: int) -> Schema | None:
    stmt = select(Schema).where(Schema.user_id == owner_id, Schema.autoid == autoid).options(selectinload(Schema.fields))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create(db: AsyncSession, owner_id: UUID, name: str, description: str) -> Schema:
    i = await own_highest_index_by_name(db, owner_id, name)

    schema = Schema(name=name, description=description, user_id=owner_id, index=i)
    db.add(schema)
    await db.flush()
    
    return schema
