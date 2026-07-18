from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING
from app.core.types.type_registry import TypeRegistry

if TYPE_CHECKING:
    from app.core.generators.base_generator import BaseGenerator


class BaseType(ABC):
    generators: dict[str, type[BaseGenerator]]
    label: str
    text_color: str
    background_color: str

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.generators = {}
        TypeRegistry.register(cls)

    @classmethod
    def register(cls, classdef: type[BaseGenerator]):
        cls.generators[classdef.__name__] = classdef
        return

    @classmethod
    def all(cls) -> list[type[BaseGenerator]]:
        return list(cls.generators.values())