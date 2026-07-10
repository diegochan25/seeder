from typing import Any
from bson import ObjectId
from app.db.document import Document


class SchemaField(Document):
    _id: ObjectId
    schema_id: ObjectId
    generator_id: ObjectId
    name: str
    options: dict[str, Any]
