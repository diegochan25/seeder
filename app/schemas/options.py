from typing import Literal

from pydantic import BaseModel


class RandomUUIDOptions(BaseModel):
    version: Literal[1, 3, 4, 5, 6, 7]
    name: str | None = None
    namespace: str | None = None
    as_uuid: bool = False
