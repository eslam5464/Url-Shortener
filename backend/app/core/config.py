import json
import os
import tomllib
from enum import StrEnum
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class LogLevel(StrEnum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Environment(StrEnum):
    development = "dev"
    production = "prd"


PROJECT_DIR = Path(__file__).parent.parent.parent

with open(f"{PROJECT_DIR}{os.sep}pyproject.toml", "rb") as f:
    PYPROJECT_CONTENT = tomllib.load(f)["tool"]["poetry"]


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    app_name: str = PYPROJECT_CONTENT["name"]
    app_version: str = PYPROJECT_CONTENT["version"]
    app_description: str = PYPROJECT_CONTENT["description"]
    api_v1_str: str = "/api/v1"

    host: str = os.getenv("BACKEND_HOST")
    port: int = os.getenv("BACKEND_PORT")

    cors_origins: list[str] = json.loads(os.getenv("CORS_ORIGIN", "[]"))
    allowed_hosts: list[str] = json.loads(os.getenv("ALLOWED_HOSTS", "[]"))

    # Number of workers for uvicorn
    gunicorn_workers_count: int = 2

    # Enable uvicorn reloading
    reload_uvicorn: bool = False

    # Current working environment
    current_environment: Environment = os.getenv("ENVIRONMENT", Environment.development)
    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_host: str = os.getenv("POSTGRES_HOST")
    db_port: int = os.getenv("POSTGRES_PORT")
    db_user: str = os.getenv("POSTGRES_USER")
    db_pass: str = os.getenv("POSTGRES_PASSWORD")
    db_base: str = os.getenv("POSTGRES_DB")
    db_schema: str = os.getenv("POSTGRES_DB_SCHEMA")
    db_echo: bool = False

    # Variables for Redis
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = os.getenv("REDIS_PORT")
    redis_user: str | None = os.getenv("REDIS_USER")
    redis_pass: str | None = os.getenv("REDIS_PASS")
    redis_base: int | None = None

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.current_environment == Environment.development:
            return f"http://{self.host}:{self.port}"

        return f"https://{self.host}"

    @computed_field  # type: ignore[misc]
    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @computed_field  # type: ignore[misc]
    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )


settings = Settings()  # type: ignore
