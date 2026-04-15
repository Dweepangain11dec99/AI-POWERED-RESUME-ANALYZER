"""One-step development setup helper.

- Installs Python dependencies from `requirements.txt` using the active interpreter
- Runs `scripts/install_spacy_models.py` to fetch common spaCy models

Run from the project root (inner folder):

    python scripts/setup_dev_env.py

This is intentionally simple — it executes pip install and then the spaCy installer.
"""
import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REQ = os.path.join(ROOT, 'requirements.txt')
INSTALL_SCRIPT = os.path.join(ROOT, 'scripts', 'install_spacy_models.py')


def run(cmd, cwd=None):
    logger.info('Running: %s', ' '.join(cmd))
    subprocess.check_call(cmd, cwd=cwd or ROOT)


def install_requirements():
    if not os.path.exists(REQ):
        logger.warning('requirements.txt not found at %s', REQ)
        return
    run([sys.executable, '-m', 'pip', 'install', '-r', REQ])


def run_spacy_installer():
    if os.path.exists(INSTALL_SCRIPT):
        run([sys.executable, INSTALL_SCRIPT])
    else:
        logger.warning('install_spacy_models.py not found at %s', INSTALL_SCRIPT)


if __name__ == '__main__':
    try:
        install_requirements()
    except Exception as e:
        logger.exception('Failed to install requirements: %s', e)
        sys.exit(1)

    try:
        run_spacy_installer()
    except Exception as e:
        logger.exception('Failed to run spaCy installer: %s', e)
        sys.exit(1)

    logger.info('Development setup finished. You may continue with DB init and starting the app.')
