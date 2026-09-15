from abc import ABC
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsGeneration(Protocol):
    name: str
    options: dict

    def generate(self): 
        ...

class SupportsHTMLUserInput[T](ABC):
    __selector__: str

    def to_html(pyvalue: T) -> str:
        return pyvalue

    def to_python(htmlvalue: str) -> T:
        return htmlvalue