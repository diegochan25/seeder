from datetime import datetime
from typing import Any
from bson import ObjectId
from app.db.document import Document


class Session(Document):
    _id: ObjectId
    uid: ObjectId
    ip_address: str
    user_agent: str
    created_at: datetime
    expires_at: datetime
    data: dict[str, Any]