from pydantic_settings import BaseSettings, SettingsConfigDict


class Secrets(BaseSettings):
    """
    Loads secrets/configuration from the environment.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: str
    EMBEDDING_MODEL_NAME: str
    LOG_LEVEL: str = "INFO"
    CALLBACK_URL: str
    TOP_K: int = 5


secrets = Secrets()
