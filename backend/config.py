from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str
    chat_id: str
    database_url: str = "sqlite:///./leads.db"
    cors_origins: str = "http://localhost:5173,http://localhost:4173"

    # Telegram API base URL. Default is the official endpoint.
    # You can override it to use a proxy/mirror, e.g. a Cloudflare Worker:
    # https://empty-dew-4b05.hipster-hop123.workers.dev/
    telegram_api_url: str = "https://api.telegram.org/"

    # Optional SOCKS5 proxy URL for the Telegram bot session, e.g.:
    # socks5://user:password@host:port
    proxy_url: str | None = None

    # SMTP settings for email notifications (Yandex: smtp.yandex.ru:465)
    smtp_host: str = "smtp.yandex.ru"
    smtp_port: int = 465
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    smtp_to: str | None = None


settings = Settings()
