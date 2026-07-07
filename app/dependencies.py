from typing import Annotated
from fastapi import Depends
from inflect import engine

def get_inflect_engine():
    return engine()

RequiresInflect = Annotated[engine, Depends(get_inflect_engine)]