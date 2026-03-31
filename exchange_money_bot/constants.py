"""Non-secret defaults (locale, limits). Secrets and deployment URLs stay in config / .env."""

# BCP 47 style; add matching module under locales/ when introducing a language.
DEFAULT_LOCALE = "fa"

# Telegram inline button label max length (API limit 64 bytes; we stay conservative).
TELEGRAM_INLINE_BUTTON_LABEL_MAX = 64
