from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str


settings = Settings()