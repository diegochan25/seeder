from bson import ObjectId
from app.db.document import Document

class SchemaType(Document):
    _id: ObjectId
    name: str