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
    # OpenRouter настройки
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    MAX_TOKENS: int = 512
    CONNECTION_TIMEOUT: int = 30

    # Настройки кэша
    CACHE_TTL: int = 10
    CACHE_MAXSIZE: int = 1

    # Настройки параметров ретраев
    MAX_RETRIES: int = 3
    RETRY_MULTIPLIER: int = 1
    MIN_RETRY_DELAY: int = 1
    MAX_RETRY_DELAY: int = 60

    # Настройки клиента
    MAX_CONNECTIONS: int = 100
    MAX_KEEPALIVE: int = 40
    READ_TIMEOUT: int = 100
    CONNECT_TIMEOUT: int = 20
    WRITE_TIMEOUT: int = 100
    POOL_TIMEOUT: int = 50


settings = Settings()
