from bson import ObjectId
from datetime import datetime
from app.db.document import Document


class User(Document):
    _id: ObjectId
    email: str
    password_hash: str
    pfp_url: str
    created_at: datetime
    updated_at: datetime