import re
from abc import ABC
from dataclasses import dataclass, field
from typing import ClassVar, Protocol, runtime_checkable
from markupsafe import Markup, escape


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
        tag, _, rest = self.__selector__.partition('[')
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', rest))
        attrs['name'] = self.name
        attrs['id'] = self.name
        if form_id is not None:
            attrs['form'] = form_id
        if not self.optional:
            attrs['required'] = 'required'
        if self.default is not None:
            attrs['value'] = self.to_html(self.default)

        attr_str = ' '.join(f'{key}="{escape(value)}"' for key, value in attrs.items())
        return Markup(f'<{tag} {attr_str}>')


@runtime_checkable
class SupportsGeneration(Protocol):
    name: str
    type: str
    options: list[SupportsHTMLUserInput]

    def generate(self):
        ...