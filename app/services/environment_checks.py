"""
Environment and dependency checks
"""
import logging
import os
from typing import List

logger = logging.getLogger(__name__)


def run_startup_checks() -> None:
    """Run startup environment checks"""
    checks_passed = True
    
    # Check required environment variables
    required_vars = ["JWT_SECRET", "HF_TOKEN", "DATABASE_URL"]
    for var in required_vars:
        if not os.getenv(var):
            logger.warning(f"Missing environment variable: {var}")
            checks_passed = False
    
    # Check spaCy model
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning("spaCy model 'en_core_web_sm' not found. Download with: python -m spacy download en_core_web_sm")
    except ImportError:
        logger.warning("spaCy not installed")
    
    # Check Tesseract
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        logger.info("Tesseract OCR found")
    except Exception as e:
        logger.warning(f"Tesseract OCR not found: {e}")
    
    # Check Hugging Face token
    if not os.getenv("HF_TOKEN"):
        logger.warning("HF_TOKEN not set - HuggingFace features will not work")
        checks_passed = False
    
    if checks_passed:
        logger.info("All startup checks passed")
    else:
        logger.info("Some startup checks had warnings - application may have limited functionality")
