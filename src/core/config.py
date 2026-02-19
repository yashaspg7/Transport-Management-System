from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Transport-Management-System"
    VERSION: str = "0.1.0"

    ENVIRONMENT: str
    DATABASE_URL: str
    SECRET_KEY: str

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600

    DEBUG: bool = False

    CORS_ORIGINS: list[str] | str = []

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            if not v:
                return []
            return [origin.strip() for origin in v.split(",")]
        return v


settings = Settings()  # pyright: ignore [reportCallIssue]
