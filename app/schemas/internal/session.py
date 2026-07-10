from typing import Any

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Session(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: ObjectId = Field(alias='_id')
    ip_address: str
    user_agent: str
    data: dict[str, Any] | None