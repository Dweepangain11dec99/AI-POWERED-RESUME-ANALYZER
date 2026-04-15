"""
Lightweight speech-to-text wrapper with lazy backends.
Supports Whisper (if installed) or raises informative error.
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def transcribe_audio(path: str, model: str = "small", language: Optional[str] = None) -> str:
    """Transcribe audio file at `path` using an available backend.

    - Tries `whisper` (OpenAI) package first, then `faster_whisper` if available.
    - If none available, raises RuntimeError with instructions.
    """
    # Try whisper
    try:
        import whisper
        model_obj = whisper.load_model(model)
        # whisper returns dict with 'text'
        result = model_obj.transcribe(path, language=language) if language else model_obj.transcribe(path)
        return result.get('text', '')
    except Exception:
        logger.debug("whisper not available or failed; trying faster_whisper", exc_info=True)

    try:
        from faster_whisper import WhisperModel
        # faster_whisper model sizes: tiny, base, small, medium, large
        w = WhisperModel(model, device="cpu", compute_type="int8_float16")
        segments, info = w.transcribe(path, language=language) if language else w.transcribe(path)
        text = "\n".join([s.text for s in segments])
        return text
    except Exception:
        logger.debug("faster_whisper not available or failed", exc_info=True)

    # No backend available
    raise RuntimeError(
        "No speech-to-text backend available. Install 'whisper' or 'faster-whisper' and try again.\n"
        "Example: pip install -U openai-whisper or pip install -U faster-whisper"
    )
