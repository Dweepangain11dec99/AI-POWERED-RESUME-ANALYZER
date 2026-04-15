"""Light wrapper for `sentence_transformers.SentenceTransformer`.

Provides a stable symbol `SentenceTransformer` so other modules can import
`from .sentence_transformers import SentenceTransformer` without importing
the heavy package at module import time (wrapper still imports the package
when constructed).
"""
try:
    from sentence_transformers import SentenceTransformer as _ST

    class SentenceTransformer:
        def __init__(self, model_name: str):
            self._model = _ST(model_name)

        def encode(self, texts, convert_to_numpy: bool = False):
            return self._model.encode(texts, convert_to_numpy=convert_to_numpy)

except Exception as e:
    class SentenceTransformer:
        def __init__(self, model_name: str):
            raise ImportError("sentence-transformers not available: %s" % e)
