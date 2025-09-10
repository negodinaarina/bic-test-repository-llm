from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve(strict=True).parent

BASE_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = BASE_DIR.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARKS_DIR = BASE_DIR.parent / "benchmarks"
BENCHMARKS_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR.parent / ".env", case_sensitive=True, extra="allow"
    )

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    CONNECTION_TIMEOUT: int = 60
    CACHE_TTL: int = 10
    CACHE_MAXSIZE: int = 1
    MAX_TOKENS: int = 512

settings = Settings()
