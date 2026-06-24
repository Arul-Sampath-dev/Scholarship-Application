from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MicrosoftSettings(BaseSettings):
    client_id: str
    client_secret: str
    server_metadata_url: str

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="MICROSOFT_", extra="ignore"
    )


class GitHubSettings(BaseSettings):
    client_id: str
    client_secret: str
    authorize_url: str
    access_token_url: str
    api_base_url: str

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="GITHUB_", extra="ignore"
    )


class GoogleSettings(BaseSettings):
    client_id: str
    client_secret: str
    server_metadata_url: str

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="GOOGLE_", extra="ignore"
    )


class JWTSettings(BaseSettings):
    secret: str
    algorithm: str
    seconds: int

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="JWT_", extra="ignore"
    )


class DatabaseSettings(BaseSettings):
    name: str
    host: str
    port: int
    password: str
    user: str
    min_conn: int
    max_conn: int

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="DATABASE_", extra="ignore"
    )


class Settings(BaseModel):
    database: Annotated[DatabaseSettings, Field(default_factory=DatabaseSettings)]  # type: ignore[arg-type]
    jwt: Annotated[JWTSettings, Field(default_factory=JWTSettings)]  # type: ignore[arg-type]
    google: Annotated[GoogleSettings, Field(default_factory=GoogleSettings)]  # type: ignore[arg-type]
    github: Annotated[GitHubSettings, Field(default_factory=GitHubSettings)]  # type: ignore[arg-type]
    microsoft: Annotated[MicrosoftSettings, Field(default_factory=MicrosoftSettings)]  # type: ignore[arg-type]


settings = Settings()  # type: ignore[call-arg]
