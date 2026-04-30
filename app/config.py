from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int

    # async (FastAPI)
    DATABASE_URL: str # yo chai async (FastAPI) ko lagi ho, FastAPI le async URL support gardaicha

    SYNC_DATABASE_URL: str # yo chai sync (Alembic) ko lagi ho, Alembic le async URL support gardaina

    REDIS_HOST: str
    REDIS_PORT: int   

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )


config = Settings()