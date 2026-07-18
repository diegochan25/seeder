from datetime import datetime, timezone
from random import randint
from typing import override
from app.core.generators.base_generator import BaseGenerator
from app.core.options.date_option import DateOption


class RandomTimestamp(BaseGenerator, type_key='Date'):
    label = 'Random timestamp'
    options = [
        DateOption('from', label='From', default=datetime.fromtimestamp(0)), 
        DateOption('to', label='To', default=datetime.now())
    ]

    @override
    def generate(self):
        return randint(0, int(datetime.now(timezone.utc).timestamp()))