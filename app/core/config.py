from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "Personal Finance API"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    db_host: str
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str
    db_sslmode: str = "require"

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?sslmode={self.db_sslmode}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
