from datetime import datetime
from typing import override
from app.core.generators.base_generator import BaseGenerator
from app.core.options.text_option import TextOption
from app.core.options.number_option import NumberOption
from app.core.options.range_option import RangeOption
from app.core.options.boolean_option import BooleanOption
from app.core.options.date_option import DateOption


class KitchenSink(BaseGenerator, type_key='String'):
    """Fake generator exercising every option type, for visualizing the option picker."""
    label = 'Kitchen sink (demo)'
    options = [
        TextOption('prefix', label='Prefix', default='sample_'),
        NumberOption('length', label='Length', default=10, min=1, max=100, step=1),
        RangeOption('weight', label='Weight', default=50, required=True, min=0, max=100, step=1),
        BooleanOption('uppercase', label='Uppercase', default=False),
        DateOption('as_of', label='As of', default=datetime.now()),
    ]

    @override
    def generate(self):
        return 'sample_value'
