from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    telegram_bot_token: Optional[str] = None
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    """Async SQLAlchemy URL, e.g. postgresql+asyncpg://... or sqlite+aiosqlite:///./data/app.db"""

    api_base_url: Optional[str] = None
    """If set, the bot pings the API after upsert (optional loose coupling)."""

    start_button_1_text: str = "قصد فروش ارز و دریافت ریال دارم"
    start_button_2_text: str = "قصد خرید ارز و پرداخت ریال دارم"
    start_button_1_reply: str = (
        "شما گزینهٔ «فروش ارز و دریافت ریال» را انتخاب کردید. "
        "به‌زودی ادامهٔ فرآیند را اینجا اضافه می‌کنیم."
    )
    start_button_2_reply: str = (
        "شما گزینهٔ «خرید ارز و پرداخت ریال» را انتخاب کردید. "
        "به‌زودی ادامهٔ فرآیند را اینجا اضافه می‌کنیم."
    )


settings = Settings()
