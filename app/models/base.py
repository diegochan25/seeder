import uuid
import inflect
from datetime import datetime
from case_convert import snake_case
from sqlalchemy import UUID, BigInteger, DateTime, Identity, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

engine = inflect.engine()


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
    def __tablename__(cls):
        return snake_case(engine.plural(cls.__name__))
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    autoid: Mapped[int] = mapped_column(BigInteger, Identity(always=True), unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())