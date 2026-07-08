from bson import ObjectId
from typing import TypedDict

class GenerationCount(TypedDict):
    schema_id: ObjectId
    count: int