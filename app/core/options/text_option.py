from app.core.options.base_option import BaseOption
from dataclasses import dataclass

@dataclass
class TextOption(BaseOption):
    default: str | None = None