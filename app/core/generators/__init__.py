from app.core.protocols import SupportsGeneration
from app.core.generators.strings import RandomUUID

GENERATORS: dict[str, type[SupportsGeneration]] = {gen.name: gen for gen in [RandomUUID]}
