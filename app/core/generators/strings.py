from abc import ABC
from enum import StrEnum

from app.core.option_types import Select, Textbox


class StringGenerator(ABC):
    type = 'string'

    def generate(self):
        ...

class UUIDVersions(StrEnum):
    UUID1 = '1'
    UUID3 = '3'
    UUID4 = '4'
    UUID5 = '5'
    UUID6 = '6'
    UUID7 = '7'

class RandomUUID(StringGenerator):
    name = 'uuid'
    label = 'UUID'

    options = [
        Select(name='version', label='Version', choices=UUIDVersions, default=UUIDVersions.UUID4),
        Textbox(name='name', label='Name', optional=True),
        Textbox(name='namespace', label='Namespace', optional=True),
    ]

    def generate(self):
        ...