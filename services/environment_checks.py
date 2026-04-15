"""Environment checks for runtime dependencies (spaCy models, Tesseract binary).

Call `run_startup_checks()` from app startup to log actionable warnings.
"""
import logging
import shutil
from typing import List

logger = logging.getLogger(__name__)


def check_tesseract() -> bool:
    """Return True if tesseract binary is available on PATH."""
    path = shutil.which('tesseract')
    if path:
        logger.info('Tesseract found at %s', path)
        return True
    logger.warning('Tesseract not found on PATH. OCR via pytesseract will fail unless Tesseract is installed. See: https://github.com/tesseract-ocr/tesseract')
    return False


def check_spacy_models(models: List[str] = None) -> List[str]:
    """Check availability of spaCy models. Returns list of missing models."""
    try:
        import spacy
    except Exception:
        logger.warning('spaCy not installed; NLP features will be limited. Install via `pip install spacy`.')
        return models or []

    if models is None:
        models = ['en_core_web_sm', 'es_core_news_sm', 'fr_core_news_sm']

    missing = []
    for m in models:
        try:
            spacy.load(m)
            logger.info('spaCy model available: %s', m)
        except Exception:
            logger.warning('spaCy model missing: %s. Install with `python -m spacy download %s`', m, m)
            missing.append(m)
    return missing


def run_startup_checks():
    """Run a few checks and log warnings for the operator/admin."""
    logger.info('Running startup environment checks...')
    check_tesseract()
    missing = check_spacy_models()
    if missing:
        logger.info('Missing spaCy models: %s', missing)
        logger.info('You can run `python scripts/install_spacy_models.py` to install common models.')
    else:
        logger.info('spaCy models all available.')
