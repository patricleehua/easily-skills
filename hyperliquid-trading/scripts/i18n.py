"""Internationalization module for Hyperliquid CLI."""

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

# Locales directory
LOCALES_DIR = Path(__file__).parent.parent / "locales"

# Supported languages
SUPPORTED_LANGUAGES = ["en", "zh-CN"]

# Default language
DEFAULT_LANGUAGE = "en"


@lru_cache(maxsize=10)
def load_translations(lang: str) -> dict:
    """Load translations for a language.

    Args:
        lang: Language code (e.g., "en", "zh-CN")

    Returns:
        Translation dictionary
    """
    path = LOCALES_DIR / f"{lang}.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def get_nested_value(data: dict, key: str) -> str | dict:
    """Get nested value from dictionary using dot notation.

    Args:
        data: Dictionary to search
        key: Dot-separated key (e.g., "account.title")

    Returns:
        Value or empty dict if not found
    """
    keys = key.split(".")
    value = data
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, {})
        else:
            return key
    return value if isinstance(value, str) else key


def t(key: str, lang: Optional[str] = None, **kwargs) -> str:
    """Translate a key with optional formatting.

    Args:
        key: Translation key (e.g., "account.total_value")
        lang: Language code (defaults to HL_LANGUAGE env or "en")
        **kwargs: Format variables

    Returns:
        Translated and formatted string

    Example:
        >>> t("account.value", value=100.50)
        'Account Value: $100.50'
    """
    # Get language from parameter, env var, or default
    if lang is None:
        lang = os.getenv("HL_LANGUAGE", DEFAULT_LANGUAGE)

    # Fallback to en if language not supported
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    translations = load_translations(lang)
    text = get_nested_value(translations, key)

    # Fallback to English if key not found
    if text == key and lang != "en":
        en_translations = load_translations("en")
        en_text = get_nested_value(en_translations, key)
        if en_text != key:
            text = en_text

    # Format with variables if provided
    if kwargs and text != key:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text

    return text


def get_available_languages() -> list[str]:
    """Get list of available languages."""
    return SUPPORTED_LANGUAGES.copy()


def detect_language() -> str:
    """Detect system language.

    Returns:
        Detected language code or default
    """
    # Check environment variable first
    env_lang = os.getenv("HL_LANGUAGE")
    if env_lang and env_lang in SUPPORTED_LANGUAGES:
        return env_lang

    # Try to detect from system locale
    import locale

    try:
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            # Map locale to supported language
            if system_locale.startswith("zh_CN") or system_locale.startswith("zh-CN"):
                return "zh-CN"
            elif system_locale.startswith("zh_TW") or system_locale.startswith("zh-TW"):
                return "zh-CN"  # Use simplified Chinese for now
    except Exception:
        pass

    return DEFAULT_LANGUAGE
