import logging
from typing import Optional

try:
    from langdetect import detect
    _LANGDETECT_AVAILABLE = True
except Exception:
    detect = None  # type: ignore
    _LANGDETECT_AVAILABLE = False

logger = logging.getLogger(__name__)


def detect_language(text: str) -> str:
    """Detect language code (e.g. 'en', 'es') for the given text.

    Falls back to 'en' if detection fails or the library isn't available.
    """
    if not text:
        return "en"
    if not _LANGDETECT_AVAILABLE:
        logger.debug("langdetect not available; defaulting to 'en'")
        return "en"
    try:
        lang = detect(text)
        return lang or "en"
    except Exception as e:
        logger.exception("language detection failed: %s", e)
        return "en"
