from datetime import datetime
from typing import Self
from bson import ObjectId
from app.db.document import Document

class Seed(Document):
    _id: ObjectId
    name: str
    index: int
    slug: str
    description: str
    user_id: ObjectId
    created_at: datetime
    updated_at: datetime

    @classmethod
    def with_max_index_by_name(cls, name: str) -> Self | None:
        result = cls.collection.find_one({'name': name}, sort=[('index', -1)])
        if result is None:
            return None
        return cls.of(result)