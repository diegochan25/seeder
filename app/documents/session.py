from datetime import datetime
from typing import Any
from bson import ObjectId
from pymongo import ASCENDING, IndexModel
from app.db.document import Document


class Session(Document):
    __indexes__ = [IndexModel([('expires_at', ASCENDING)], expireAfterSeconds=0)]

    _id: ObjectId
    uid: ObjectId
    ip_address: str
    user_agent: str
    created_at: datetime
    expires_at: datetime
    data: dict[str, Any]