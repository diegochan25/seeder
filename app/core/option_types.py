from datetime import date, datetime
from app.core.protocols import SupportsHTMLUserInput

class Textbox(SupportsHTMLUserInput[str]):
    pass


class Date(SupportsHTMLUserInput[date]):
    __selector__ = 'input[type="date"]'

    def to_html(pyvalue: date) -> str:
        return pyvalue.strftime('%Y-%m-%d')

    def to_python(htmlvalue: str) -> date:
        return date.fromisoformat(htmlvalue)


class DateTime(SupportsHTMLUserInput[datetime]):
    __selector__ = 'input[type="datetime-local"]'

    def to_html(pyvalue: datetime) -> str:
        return pyvalue.strftime('%Y-%m-%dT%H:%M:%S')

    def to_python(htmlvalue: str) -> datetime:
        return datetime.fromisoformat(htmlvalue)


class Number(SupportsHTMLUserInput[float]):
    __selector__ = 'input[type="number"]'

    def to_html(pyvalue: float) -> str:
        return str(pyvalue)
    def to_python(htmlvalue: str) -> float:
        return float(htmlvalue)


class Range(Number):
    pass