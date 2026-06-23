from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str
    chat_id: str
    database_url: str = "sqlite:///./leads.db"
    cors_origins: str = "http://localhost:5173,http://localhost:4173"


settings = Settings()
