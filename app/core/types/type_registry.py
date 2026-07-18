from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.generators.base_generator import BaseGenerator
    from app.core.types.base_type import BaseType


class TypeRegistry:
    types: dict[str, type['BaseType']] = {}

    @classmethod
    def all(cls) -> list[type['BaseType']]:
        return list(cls.types.values())

    @classmethod
    def generators(cls) -> dict[str, list[type['BaseGenerator']]]:
        groups = {}
        for key, value in cls.types.items():
            groups[key] = value.all() or []
        return groups

    @classmethod
    def register(cls, classdef: type['BaseType']):
        cls.types[classdef.__name__] = classdef
        return