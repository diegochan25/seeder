from bson import ObjectId
from app.db.document import Document

class SchemaGenerator(Document):
    _id: ObjectId
    type_id: ObjectId
    name: str