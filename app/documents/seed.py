from datetime import datetime
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