"""Lightweight i18n: load strings by locale key. Add `locales/en.py` and register in _TABLES to add English."""

from __future__ import annotations

from typing import Any, Optional

from exchange_money_bot.constants import DEFAULT_LOCALE
from exchange_money_bot.locales import fa as locale_fa

_TABLES: dict[str, dict[str, str]] = {
    "fa": locale_fa.STRINGS,
}


def t(key: str, default: Optional[str] = None, *, locale: Optional[str] = None, **kwargs: Any) -> str:
    """
    Resolve a message for `key` in `locale` (default: constants.DEFAULT_LOCALE).
    Missing keys fall back to `default`, then to the key string.
    Use kwargs for str.format placeholders in the template.
    """
    loc = locale or DEFAULT_LOCALE
    table = _TABLES.get(loc) or _TABLES["fa"]
    template = table.get(key)
    if template is None:
        template = default if default is not None else key
    if kwargs:
        return template.format(**kwargs)
    return template
