from datetime import datetime
from bson import ObjectId
from app.db.document import Document
from app.documents.generation_count import GenerationCount


class SeedGeneration(Document):
    _id: ObjectId
    seed_id: ObjectId
    format_id: ObjectId
    counts: list[GenerationCount]
    generated_at: datetime