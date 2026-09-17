from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum
from markupsafe import Markup, escape
from app.core.html import Selector
from app.core.protocols import SupportsHTMLUserInput


@dataclass
class Textbox(SupportsHTMLUserInput[str]):
    __selector__ = 'input[type="text"].form-control'


@dataclass
class Date(SupportsHTMLUserInput[date]):
    __selector__ = 'input[type="date"].form-control'

    def to_html(self, pyvalue: date) -> str:
        return pyvalue.strftime('%Y-%m-%d')

    def to_python(self, htmlvalue: str) -> date:
        return date.fromisoformat(htmlvalue)


@dataclass
class DateTime(SupportsHTMLUserInput[datetime]):
    __selector__ = 'input[type="datetime-local"].form-control'

    def to_html(self, pyvalue: datetime) -> str:
        return pyvalue.strftime('%Y-%m-%dT%H:%M:%S')

    def to_python(self, htmlvalue: str) -> datetime:
        return datetime.fromisoformat(htmlvalue)


@dataclass
class Number(SupportsHTMLUserInput[float]):
    __selector__ = 'input[type="number"].form-control'

    def to_html(self, pyvalue: float) -> str:
        return str(pyvalue)

    def to_python(self, htmlvalue: str) -> float:
        return float(htmlvalue)


@dataclass
class Select(SupportsHTMLUserInput[str]):
    __selector__ = 'select.form-control'
    choices: type[StrEnum]

    def render(self, form_id: str | None = None) -> Markup:
        sel = Selector.from_selector(self.__selector__)
        sel.id = self.name
        sel.attr.name = self.name
        if form_id is not None:
            sel.attr.form = form_id
        if not self.optional:
            sel.attr.required = True

        options = ''.join(
            f'<option value="{escape(choice.value)}" {"selected" if choice == self.default else ""}>{escape(choice.name)}</option>'
            for choice in self.choices
        )
        return Markup(sel.tag(options))


@dataclass
class Toggle(SupportsHTMLUserInput[bool]):
    __selector__ = 'input[type="checkbox"].toggle'

    def to_html(self, pyvalue: bool) -> str:
        pass

    def to_python(self, htmlvalue: str | None) -> bool:
        if htmlvalue is None:
            return False
        return True

    def render(self, form_id: str | None = None) -> Markup:
        sel = Selector.from_selector(self.__selector__)
        sel.id = self.name
        sel.attr.name = self.name
        if form_id is not None:
            sel.attr.form = form_id
        if self.default:
            sel.attr.checked = True
        return Markup(sel.tag())

@dataclass
class Range(Number):
    __selector__ = 'input[type="range"].slider'
    min: float = 0.0
    max: float = 100.0
    step: float = 1.0

    def render(self, form_id: str | None = None) -> Markup:
        sel = Selector.from_selector(self.__selector__)
        sel.id = self.name
        sel.attr.name = self.name
        sel.attr.min = self.min
        sel.attr.max = self.max
        sel.attr.step = self.step
        if form_id is not None:
            sel.attr.form = form_id
        if not self.optional:
            sel.attr.required = True
        if self.default is not None:
            sel.attr.value = self.to_html(self.default)
        return Markup(sel.tag())