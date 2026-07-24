from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "taskflow-api"
    DEBUG: bool = True
    DATABASE_URL: str 
    SECRET_KEY: str 
    OPENAI_API_KEY: str
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()    