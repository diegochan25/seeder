from abc import ABC
from typing import Any
from dataclasses import dataclass

@dataclass
class BaseOption(ABC):
    name: str
    label: str
    default: Any | None
    required: bool = False

    def to_value(self, val: Any) -> Any:
        """
        Transforms data from Python's format 
        to a valid HTML input value.
        """
        pass

    def to_field(self, val: Any) -> Any:
        """
        Transforms data from an HTML input 
        value to a valid Python object.
        """
        if not val:
            if self.required:
                raise ValueError(f"Required option '{self.name}' was not provided a value.")
            elif self.default:
                return self.default
            else:
                pass