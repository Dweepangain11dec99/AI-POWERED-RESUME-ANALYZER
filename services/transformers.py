"""Tiny wrapper exposing `pipeline` from Hugging Face `transformers`.

Uses a simple function `pipeline(task)` which will attempt to import and
instantiate the HF pipeline. If `transformers` isn't installed, an ImportError
is raised when called.
"""
try:
    from transformers import pipeline as _hf_pipeline

    def pipeline(task: str):
        return _hf_pipeline(task)

except Exception as e:
    def pipeline(task: str):
        raise ImportError("transformers not available: %s" % e)
