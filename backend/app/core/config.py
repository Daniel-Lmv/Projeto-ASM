from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Configuração da aplicação
    app_name: str = Field(alias="APP_NAME")
    app_env: str = Field(alias="APP_ENV")
    debug: bool = Field(alias="DEBUG")

    # Banco de dados
    db_host: str = Field(alias="DB_HOST")
    db_port: int = Field(alias="DB_PORT")
    db_name: str = Field(alias="DB_NAME")
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD")

    # Segurança
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()