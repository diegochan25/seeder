from random import random
from typing import override
from app.core.generators.base_generator import BaseGenerator
from app.core.options.boolean_option import BooleanOption
from app.core.options.range_option import RangeOption


class Random(BaseGenerator, type_key='Boolean'):
    label = 'Random boolean'
    options = [
        BooleanOption('nullable', label='Nullable', default=False),
        RangeOption('weight', label='True/False proportion', default=50, required=True, min=0, max=100, step=1)
    ]
    
    @override
    def generate(self):
        return random() >= 0.5