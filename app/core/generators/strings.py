from abc import ABC
from enum import StrEnum
import random as r
import uuid
from app.core.option_types import Range, Select, Textbox, Toggle


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
        Textbox(name='uuid_name', label='Name', optional=True),
        Textbox(name='namespace', label='Namespace', optional=True),
        Toggle(name='optional', label='Optional', default=False),
        Range(name='null_ratio', label='Null ratio (approximate)', step=5.0, default=10.0, optional=True)
    ]

    def generate(self, options: dict):
        version = options.get('version')
        name = options.get('name')
        namespace = options.get('namespace')
        optional = options.get('optional')
        null_ratio = options.get('null_ratio', 10.0)

        prob = 1.0 - null_ratio / 100 if optional else 1.0

        if (version == '5' or version == '6') and (not name or not namespace):
            raise ValueError('UUID versions 5 and 6 require a name and namespace to be passed in')

        match (version):
            case '1':
                return None if r.random() >= prob else uuid.uuid1()
            case '3':
                return None if r.random() >= prob else uuid.uuid3()
            case '4':
                return None if r.random() >= prob else uuid.uuid4()
            case '5':
                return None if r.random() >= prob else uuid.uuid5(name=name, namespace=namespace)
            case '6':
                return None if r.random() >= prob else uuid.uuid6(name=name, namespace=namespace)
            case '7':
                return None if r.random() >= prob else uuid.uuid7()