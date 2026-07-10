from abc import ABC
from copy import deepcopy
from typing import Any, Self
from bson import ObjectId
from case_convert import snake_case
from pymongo import MongoClient, ReturnDocument
from pymongo.cursor import Cursor
from inflect import engine
from pymongo.database import Database
from pymongo.collection import Collection
from app.db.client import client


class Document(ABC):
    __database_name__ = 'seeder'
    client: MongoClient
    inflect = engine()
    collection_name: str

    db: Database
    collection: Collection
    _id: ObjectId

    def __init_subclass__(cls):
        cls.client = client
        cls.collection_name = snake_case(cls.inflect.plural(cls.__name__))

        cls.db = client.get_database(cls.__database_name__)
        cls.collection = cls.db.get_collection(cls.collection_name)

    def __init__(self, **kwargs: Any):
        self._id = kwargs.pop('_id', None) or ObjectId()
        for name, value in kwargs.items():
            setattr(self, name, value)

    def serialize(self) -> dict[str, Any]:
        return {name: getattr(self, name, None) for name in self.__class__.__annotations__}

    @classmethod
    def of(cls, document: dict[str, Any]):
        kwargs = deepcopy(document)
        keys = document.keys()
        for name in cls.__annotations__.keys():
            if name not in keys:
                kwargs[name] = None
        return cls(**kwargs)
    
    @classmethod
    def cursor(cls, limit: int = 0, offset: int = 0) -> Cursor:
        limit = max(limit, 0)
        offset = max(offset, 0)
        return cls.collection.find().skip(offset).limit(limit)
    
    @classmethod
    def list(cls, limit: int = 0, offset: int = 0) -> list[Self]:
        return [cls.of(document) for document in list(cls.cursor(limit, offset))]

    @classmethod
    def count(cls) -> int:
        return cls.collection.count_documents({}) or 0

    @classmethod
    def find_by_id(cls, id: ObjectId) -> Self | None:
        result = cls.collection.find_one({'_id': id})
        if result is None:
            return None
        return cls.of(result)

    @classmethod
    def find_by(cls, **kwargs: Any) -> Self | None:
        result = cls.collection.find_one(kwargs)
        if result is None:
            return None
        return cls.of(result)
    
    @classmethod
    def cursor_by(cls, **kwargs: Any) -> Cursor:
        return cls.collection.find(kwargs)
    
    @classmethod
    def list_by(cls, **kwargs: Any) -> list[Self]:
        return [cls.of(document) for document in list(cls.cursor_by(**kwargs))]

    def exists(self) -> bool:
        return self.collection.count_documents({'_id': self._id}) == 1

    def save(self) -> Self:
        self.collection.find_one_and_update(
            {'_id': self._id},
            {'$set': self.serialize()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return self
    
    def delete(self) -> bool:
        try:
            result = self.collection.delete_one({ '_id': self._id })
            return result.deleted_count == 1
        except:
            return False