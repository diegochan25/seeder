from app.core.options.base_option import BaseOption
from dataclasses import dataclass

@dataclass
class NumberOption(BaseOption):
    default: float | None = None
    min: float | None = None
    max: float | None = None
    step: float = 1.0