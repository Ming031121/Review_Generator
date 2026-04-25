from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "ReviewPal API"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = False

    MODEL_NAME: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = Field(..., min_length=10)

    MAX_OUTPUT_TOKENS: int = 300
    REQUEST_TIMEOUT_SECONDS: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()