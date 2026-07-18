from abc import ABC, abstractmethod
from app.core.options.base_option import BaseOption
from app.core.types.type_registry import TypeRegistry


class BaseGenerator(ABC):
    label: str
    options: list[BaseOption]

    @classmethod
    def __init_subclass__(cls, type_key: str | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if type_key is None:
            return
        owner = TypeRegistry.types.get(type_key)
        if owner is None:
            raise ValueError(
                "Cannot register generator '{}': type '{}' is not registered yet. "
                "Make sure app.core.types is fully imported before app.core.generators.".format(
                    cls.__name__, type_key
                )
            )
        owner.register(cls)
        if not hasattr(cls, 'options'):
            cls.options = []

    @abstractmethod
    def generate(self):
        pass