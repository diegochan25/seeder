from copy import deepcopy
import re
from typing import Generator, Any, Self
from markupsafe import escape
from app.core.utils import ReadonlyKVP


class HTMLAttributes:
    _name: str
    _storage: dict[str, str | bool]

    def __init__(self, name: str = "attributes"):
        self._storage = {}
        self._name = name

    def __getattr__(self, name) -> str | bool:
        if name.startswith("_"):
            raise AttributeError(name)
        value = self._storage.get(name)
        if value is None:
            raise AttributeError(f"HTML Element {self._name} does not contain the key '{name}'.")
        return value

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            self._storage[name] = value

    def __delattr__(self, name):
        del self._storage[name]

    def __iter__(self) -> Generator[ReadonlyKVP[str, str | bool], Any, None]:
        for key, value in self._storage.items():
            yield ReadonlyKVP(key, value)

    def copy(self, d: dict[str, str | bool]):
        self._storage = deepcopy(d)

    def keys(self) -> Generator[str, Any, None]:
        for key in self._storage.keys():
            yield key

    def values(self) -> Generator[str | bool, Any, None]:
        for value in self._storage.values():
            yield value

    def items(self) -> Generator[tuple[str, str | bool], Any, None]:
        for key, value in self._storage.items():
            yield key, value

    def get(self, name: str, default=None):
        return self._storage.get(name, default)

    def __bool__(self) -> bool:
        return bool(self._storage)


class Selector:
    _element_pattern = re.compile(r"^([a-z]+)", re.IGNORECASE)
    _id_pattern = re.compile(r"#([A-Za-z][A-Za-z0-9\-_:]*)", re.IGNORECASE)
    _class_pattern = re.compile(r"\.([A-Za-z][A-Za-z0-9\-_:]*)", re.IGNORECASE)
    _attr_pattern = re.compile(r"\[([A-Za-z0-9\-_:]+)=([\"'])(.+?)\2\]", re.IGNORECASE)

    element: str
    id: str | None
    classlist: list[str]
    attr: HTMLAttributes
    data: HTMLAttributes

    def __init__(
        self,
        element: str,
        id: str | None = None,
        classlist: list[str] | None = None,
        attr: HTMLAttributes | None = None,
        data: HTMLAttributes | None = None,
    ):
        self.element = element
        self.id = id
        self.classlist = classlist if classlist is not None else []
        self.attr = attr if attr is not None else HTMLAttributes('attribute set')
        self.data = data if data is not None else HTMLAttributes('dataset')

    @classmethod
    def from_selector(cls, selector: str) -> Self:
        if not (element_matches := cls._element_pattern.findall(selector)):
            raise ValueError("Selector string does not match expected format for element name.")

        if not (element := str(element_matches[0]).strip()):
            raise ValueError("Selector element name cannot be empty.")

        id_matches = cls._id_pattern.findall(selector)
        id = id_matches[0] if id_matches else None
        classlist = cls._class_pattern.findall(selector)
        attr_items = [(t[0], t[2]) for t in cls._attr_pattern.findall(selector)]
        data_dict = {str(t[0]).removeprefix('data-'): t[1] for t in attr_items if str(t[0]).startswith('data-')}
        attr_dict = {t[0]: t[1] for t in attr_items if not str(t[0]).startswith('data-')}

        sel = cls(element, id, classlist)

        sel.data.copy(data_dict)
        sel.attr.copy(attr_dict)

        return sel

    def self_closing(self) -> bool:
        return self.element in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']

    def plain(self) -> bool:
        return not self.id and not self.classlist and not self.attr and not self.data

    def selector(self) -> str:
        sel = self.element
        if (id := self.id) is not None:
            sel += f"#{id}"
        for classname in self.classlist:
            sel += f".{classname}"
        for name, value in self.attr.items():
            sel += f"[{name}='{value}']"
        for name, value in self.data.items():
            sel += f"[data-{name}='{value}']"
        return sel

    @staticmethod
    def _render_attr(name: str, value: str | bool) -> str:
        if value is False:
            return ""
        if value is True:
            return name
        return f'{name}="{escape(value)}"'

    def _attr_string(self) -> str:
        definitions = []

        if (id := self.id) is not None:
            definitions.append(f'id="{escape(id)}"')
        if (classlist := self.classlist):
            definitions.append(f'class="{escape(" ".join(classlist))}"')
        for entry in self.attr:
            if rendered := self._render_attr(entry.key(), entry.value()):
                definitions.append(rendered)
        for entry in self.data:
            if rendered := self._render_attr(f"data-{entry.key()}", entry.value()):
                definitions.append(rendered)

        return f" {' '.join(definitions)}" if definitions else ""

    def open_tag(self) -> str:
        return f"<{self.element}{self._attr_string()}>"

    def close_tag(self) -> str:
        return "" if self.self_closing() else f"</{self.element}>"

    def tag(self, children: str = "") -> str:
        return f"{self.open_tag()}{children}{self.close_tag()}"
