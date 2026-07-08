from bson import ObjectId
from app.db.document import Document

class Schema(Document):
    _id: ObjectId
    seed_id: ObjectId
    name: str