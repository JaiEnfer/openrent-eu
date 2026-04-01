from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OpenRent EU API"
    frontend_origin: str = "http://localhost:5173"
    database_url: str = "sqlite:///./openrent.db"
    # Optional Sentry DSN (set in production .env or secrets)
    sentry_dsn: Optional[str] = None
    sentry_traces_sample_rate: float = 0.1
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()