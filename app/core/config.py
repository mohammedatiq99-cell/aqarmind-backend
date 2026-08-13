from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Aqarmind API"
    app_env: str = "development"
    allowed_origins: str = "http://localhost:5173"

    azure_openai_endpoint: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_deployment: str | None = None

    azure_search_endpoint: str | None = None
    azure_search_api_key: str | None = None
    azure_search_index: str | None = None
    azure_search_semantic_config: str | None = None

    sql_server: str | None = None
    sql_database: str | None = None
    sql_username: str | None = None
    sql_password: str | None = None
    sql_driver: str = "ODBC Driver 18 for SQL Server"

    max_input_chars: int = 6000
    max_output_tokens: int = 800
    session_question_limit: int = 25

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def origins(self) -> list[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
