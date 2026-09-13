import re
from abc import ABC
from typing import Protocol, runtime_checkable
from app.core.html import Selector

@runtime_checkable
class SupportsGeneration(Protocol):
    options: dict

    @classmethod
    def generate(cls): 
        ...

class SupportsHTMLUserInput[T](ABC):
    __selector__: str

    def to_html(pyvalue: T) -> str:
        return pyvalue

    def to_python(htmlvalue: str) -> T:
        return htmlvalue