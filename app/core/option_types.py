from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum
from markupsafe import Markup, escape
from app.core.protocols import SupportsHTMLUserInput


@dataclass
class Textbox(SupportsHTMLUserInput[str]):
    __selector__ = 'input[type="text"]'


@dataclass
class Date(SupportsHTMLUserInput[date]):
    __selector__ = 'input[type="date"]'

    def to_html(self, pyvalue: date) -> str:
        return pyvalue.strftime('%Y-%m-%d')

    def to_python(self, htmlvalue: str) -> date:
        return date.fromisoformat(htmlvalue)


@dataclass
class DateTime(SupportsHTMLUserInput[datetime]):
    __selector__ = 'input[type="datetime-local"]'

    def to_html(self, pyvalue: datetime) -> str:
        return pyvalue.strftime('%Y-%m-%dT%H:%M:%S')

    def to_python(self, htmlvalue: str) -> datetime:
        return datetime.fromisoformat(htmlvalue)


@dataclass
class Number(SupportsHTMLUserInput[float]):
    __selector__ = 'input[type="number"]'

    def to_html(self, pyvalue: float) -> str:
        return str(pyvalue)

    def to_python(self, htmlvalue: str) -> float:
        return float(htmlvalue)


@dataclass
class Select(SupportsHTMLUserInput[str]):
    __selector__ = 'select'
    choices: type[StrEnum]

    def render(self, form_id: str | None = None) -> Markup:
        attrs = f'name="{self.name}" id="{self.name}"'
        if form_id is not None:
            attrs += f' form="{form_id}"'
        if not self.optional:
            attrs += ' required'

        options = ''.join(
            f'<option value="{escape(choice.value)}" {"selected" if choice == self.default else ""}>{escape(choice.name)}</option>'
            for choice in self.choices
        )
        return Markup(f'<select {attrs}>{options}</select>')


@dataclass
class Toggle(SupportsHTMLUserInput[bool]):
    __selector__ = 'input[type="checkbox"]'

    def to_html(self, pyvalue: bool) -> str:
        pass

    def to_python(self, htmlvalue: str | None) -> bool:
        if htmlvalue is None:
            return False
        return True

    def render(self, form_id: str | None = None) -> Markup:
        attrs = f'type="checkbox" name="{self.name}" id="{self.name}"'
        if form_id is not None:
            attrs += f' form="{form_id}"'
        if self.default:
            attrs += ' checked'
        return Markup(f'<input {attrs}>')