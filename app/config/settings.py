from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)

    mongodb_uri: str
    app_port: int
    app_reload: bool


settings = Settings()