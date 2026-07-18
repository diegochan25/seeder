from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CreateField(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    generator: str
    generator_label: str
    options: dict | None = None
