from bson import ObjectId
from app.db.document import Document


class OutputFormat(Document):
    _id: ObjectId
    name: str
    label: str
    extension: str | None
    description: str | None
    sprite_url: str