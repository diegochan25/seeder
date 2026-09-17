from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.protocols import SupportsGeneration
from app.models.schema import Field


async def create(db: AsyncSession, schema_id: UUID, name: str, generator: type[SupportsGeneration], options: dict) -> Field:
    field = Field(name=name, type=generator.type, generator=generator.name, options=options, schema_id=schema_id)
    db.add(field)
    await db.flush()

    return field
