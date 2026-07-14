from typing import Self

from bson import ObjectId
from slugify import slugify
from app.db.document import Document

class Schema(Document):
    _id: ObjectId
    seed_id: ObjectId
    name: str
    index: int
    slug: str

    @classmethod
    def group_by_seed_ids(cls, seed_ids: list[ObjectId]) -> dict[ObjectId, list[Self]]:
        cursor = cls.collection.aggregate([
            {'$match': { 
                'seed_id': {'$in': seed_ids} 
            }}, 
            {'$group': {
                '_id': '$seed_id', 
                'schemas': {'$push': '$$ROOT'}
            }}
        ])

        return {doc['_id']: [cls.of(s) for s in doc['schemas']] for doc in cursor}
    
    @classmethod
    def with_max_index_by_name(cls, name: str) -> Self | None:
        result = cls.collection.find_one({'name': name}, sort=[('index', -1)])
        if result is None:
            return None
        return cls.of(result)

    @classmethod
    def next_slug_and_index_for(cls, name: str) -> tuple[str, int]:
        highest = cls.with_max_index_by_name(name)
        index = highest.index + 1 if highest else 0
        base_slug = f"{name} {index}" if index else name
        return slugify(base_slug), index