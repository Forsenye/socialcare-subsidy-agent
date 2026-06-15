from functools import lru_cache

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:  # pragma: no cover - allows import before dependencies are installed.
    BaseSettings = object
    SettingsConfigDict = dict


class Settings(BaseSettings):
    app_name: str = "SocialCare Subsidy Agent"
    environment: str = "dev"
    use_local_rag: bool = True
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = ""
    azure_openai_api_version: str = ""
    azure_ai_search_endpoint: str = ""
    azure_ai_search_index: str = ""
    azure_ai_search_key: str = ""
    foundry_project_endpoint: str = ""
    appinsights_connection_string: str = ""
    audit_log_path: str = "data/audit/audit_log.jsonl"

    if BaseSettings is not object:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore",
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
