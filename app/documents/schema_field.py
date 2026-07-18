from typing import Any
from bson import ObjectId
from app.db.document import Document


class SchemaField(Document):
    _id: ObjectId
    schema_id: ObjectId
    generator: str
    generator_label: str
    name: str
    options: dict[str, Any]
