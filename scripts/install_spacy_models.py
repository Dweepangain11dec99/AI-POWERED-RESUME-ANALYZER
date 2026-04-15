"""Utility to install common spaCy language models for the project.

Usage:
  python scripts/install_spacy_models.py        # installs defaults
  python scripts/install_spacy_models.py en es  # installs en_core_web_sm and es_core_news_sm

This script uses the active Python interpreter to run: `python -m spacy download <model>`
"""
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_MODELS = {
    'en': 'en_core_web_sm',
    'es': 'es_core_news_sm',
    'fr': 'fr_core_news_sm'
}


def install_model(model: str) -> bool:
    try:
        logger.info('Installing model: %s', model)
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', model])
        logger.info('Installed %s', model)
        return True
    except subprocess.CalledProcessError:
        logger.exception('Failed to install %s via spacy download. You may try `pip install %s` or run as admin.', model, model)
        return False


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        models = list(DEFAULT_MODELS.values())
    else:
        models = []
        for a in args:
            models.append(DEFAULT_MODELS.get(a, a))

    success = True
    for m in models:
        ok = install_model(m)
        success = success and ok

    if not success:
        logger.error('One or more models failed to install. See logs above for details.')
    else:
        logger.info('All requested spaCy models installed successfully.')
