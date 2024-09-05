from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import AnyHttpUrl, Field, SecretStr, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class APMConfig(BaseSettings):
    url: AnyHttpUrl = Field(...)
    service_name: str = Field("SEARCH APM")


class DocsConfig(BaseSettings):
    doc_path: Path = Field(
        default_factory=lambda: Path(__file__).parent / "doc" / "open-api.yml"
    )

    @validator("doc_path")
    def validate_path(cls, v):
        if not v.exists():
            raise ValueError(f"The specified path does not exist: {v}")
        return v


class ElasticConfig(BaseSettings):
    password: SecretStr = Field(...)
    user: str = Field(...)
    url: AnyHttpUrl = Field(...)


class RedisConfig(BaseSettings):
    host: str = Field(default="redis")
    port: str = Field(default="6379")
    database: str = Field(default="0")
    password: SecretStr = Field(...)


class MatomoConfig(BaseSettings):
    id_site: str = Field(...)
    tracking_url: AnyHttpUrl = Field(...)


class MetadataConfig(BaseSettings):
    url_cc_json: AnyHttpUrl = Field(...)


class SentryConfig(BaseSettings):
    dsn: AnyHttpUrl = Field(...)

    @validator("dsn")
    def enforce_https(cls, v):
        if v.scheme != "https":
            raise ValueError("Sentry DSN must use HTTPS")
        return v


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
    )

    apm: APMConfig = Field(...)
    elastic: ElasticConfig = Field(...)
    env: str = Field(...)
    matomo: MatomoConfig = Field(...)
    metadata: MetadataConfig = Field(...)
    openapi: DocsConfig = Field(default_factory=DocsConfig)
    redis: RedisConfig = Field(...)
    sentry: SentryConfig = Field(...)

    @property
    def apm_config(self) -> dict[str, Any]:
        return {
            "ENVIRONMENT": self.env,
            "SERVER_URL": str(self.apm.url),
            "SERVICE_NAME": self.apm.service_name,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
