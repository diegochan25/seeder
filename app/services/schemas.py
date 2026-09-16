from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schema import Schema

async def own_highest_index_by_name(db: AsyncSession, owner_id: UUID, name: str) -> int:
    stmt = select(Schema).where(Schema.creator_id)


async def create(db: AsyncSession, owner_id: UUID, name: str, description: str) -> Schema:
    i = own_highest_index_by_name(db, owner_id, name) or 0

    schema = Schema(name=name, description=description, index=i)
    db.add(schema)
    await db.flush()
    
    return schema