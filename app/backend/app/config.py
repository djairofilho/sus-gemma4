from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GEMMA_SUS_", env_file=".env", extra="ignore")

    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="gemma3:4b")
    ollama_timeout_seconds: float = Field(default=30.0, gt=0)
    use_ollama: bool = Field(default=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
