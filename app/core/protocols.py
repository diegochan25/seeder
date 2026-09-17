from abc import ABC
from dataclasses import dataclass, field
from typing import ClassVar, Protocol, runtime_checkable
from markupsafe import Markup
from app.core.html import Selector


@dataclass
class SupportsHTMLUserInput[T](ABC):
    __selector__: ClassVar[str]

    name: str
    label: str | None = field(default=None, kw_only=True)
    optional: bool = field(default=False, kw_only=True)
    default: T | None = field(default=None, kw_only=True)

    def to_html(self, pyvalue: T) -> str:
        return pyvalue

    def to_python(self, htmlvalue: str) -> T:
        return htmlvalue

    def render(self, form_id: str | None = None) -> Markup:
        sel = Selector.from_selector(self.__selector__)
        sel.id = self.name
        sel.attr.name = self.name
        if form_id is not None:
            sel.attr.form = form_id
        if not self.optional:
            sel.attr.required = True
        if self.default is not None:
            sel.attr.value = self.to_html(self.default)

        return Markup(sel.tag())


@runtime_checkable
class SupportsGeneration(Protocol):
    name: str
    type: str
    options: list[SupportsHTMLUserInput]

    def generate(self):
        ...