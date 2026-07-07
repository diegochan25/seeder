from enum import StrEnum


class OptionType(StrEnum):
    Text = 'Text'
    Number = 'Number'
    Boolean = 'Boolean'
    Select = 'Select'
    Date = 'Date'
    Range = 'Range'