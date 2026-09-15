from typing import Self
import uuid
import inflect
from datetime import datetime
from case_convert import snake_case
from sqlalchemy import UUID, BigInteger, DateTime, Identity, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

engine = inflect.engine()

class ActiveRecord[T: 'Model']:
    db: AsyncSession
    model: type[T]

    def __init__(self, db: AsyncSession, model: type[T]):
        self.db = db
        self.model = model


    async def save(self, instance: T) -> T:
        self.db.add(instance)
        await self.db.flush()
        return instance

    async def all(self) -> list[T]:
        stmt = select(self.model)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def by_id(self, id: uuid.UUID) -> T | None:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, instance: T, **values) -> T:
        for key, value in values.items():
            setattr(instance, key, value)
        return await self.save(instance)

    async def delete(self, instance: T) -> None:
        await self.db.delete(instance)
        await self.db.flush()


class InstanceActiveRecord[T: 'Model']:
    """
    Per-instance API surface; delegates 
    all CRUD logic to StaticActiveRecord.
    """

    static: ActiveRecord[T]
    instance: T

    def __init__(self, db: AsyncSession, instance: T):
        self.static = ActiveRecord(db, type(instance))
        self.instance = instance

    async def save(self) -> T:
        return await self.static.save(self.instance)

    async def update(self, **values) -> T:
        return await self.static.update(self.instance, **values)

    async def delete(self) -> None:
        return await self.static.delete(self.instance)


class Model(DeclarativeBase):
    """
    Extending classes inherit from the Model class:

    `__tablename__: str`: The model's table name is evluated to the snake_case plural variant of the Model class's name.

    `id: uuid.UUID`: UUID Object used as the model's primary key, defaults to uuid.uuid4()

    `autoid: int`: An autoincrementing indexed big integer, for use as external identity.

    `created_at: datetime.datetime`: A datetime object that defaults to the time of creation in the database.

    `updated_at: datetime.datetime`: A datetime object that defaults to the time of creation in the database and gets refreshed on update.
    """
    
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self):
        return snake_case(engine.plural(self.__class__.__name__))
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    autoid: Mapped[int] = mapped_column(BigInteger, Identity(always=True), unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @classmethod
    def model(cls, db: AsyncSession) -> ActiveRecord[type[Self]]:
        return ActiveRecord(db, cls)

    def record(self, db: AsyncSession) -> InstanceActiveRecord[Self]:
        return InstanceActiveRecord(db, self)
