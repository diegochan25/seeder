from app.core.options.base_option import BaseOption
from dataclasses import dataclass

@dataclass
class BooleanOption(BaseOption):
    default: bool = False