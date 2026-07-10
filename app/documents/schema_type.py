from bson import ObjectId
from app.db.document import Document

class SchemaType(Document):
    _id: ObjectId
    name: str
    label: str
    text_color: str
    background_color: str