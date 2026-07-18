from datetime import datetime
from typing import override
from app.core.options.base_option import BaseOption
from dataclasses import dataclass

@dataclass
class DateOption(BaseOption):
    default: datetime | None = None
    start: datetime | None = None
    end: datetime | None = None

    @override
    def to_value(self, val: datetime) -> str:
        return val.date().isoformat()

    @override
    def to_field(self, val: str) -> datetime:
        return datetime.fromisoformat(val)
