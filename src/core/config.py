from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    database_url: str
    helius_api_key: str
    helius_auth_header: str
    helius_webhook_id: str

    model_config = SettingsConfigDict(env_file=ENV_FILE)


@lru_cache
def get_settings() -> Settings:
    return Settings()
