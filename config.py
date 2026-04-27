from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",  # points to src/.env
        extra="ignore"
    )

config = Settings()