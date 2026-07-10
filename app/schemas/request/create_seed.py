from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class CreateSeed(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    name: str
    description: str | None
    schema_name: str