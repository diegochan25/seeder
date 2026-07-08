from typing import Any
from bson import ObjectId
from app.db.document import Document
from app.documents.option_type import OptionType

class GeneratorOption(Document):
    _id: ObjectId
    generator_id: ObjectId
    name: str
    label: str
    type: OptionType
    default: Any | None
    choose_from: list[Any]