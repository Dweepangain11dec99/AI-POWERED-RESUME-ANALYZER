"""
Simple QA service for resume-based question answering.
Uses embedding-based retrieval (if available) and a fallback keyword search.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def answer_from_resume(resume_text: str, question: str, top_k_sentences: int = 3) -> str:
    """Return a short answer by retrieving the most relevant sentences.

    If `services.embedding_service` is available, use vector similarity to pick sentences.
    Otherwise, fall back to keyword matching.
    """
    if not resume_text:
        return "No resume text available."

    # Split into sentences
    import re
    sentences = [s.strip() for s in re.split(r'[\n\.!?]+', resume_text) if s.strip()]
    if not sentences:
        return resume_text

    try:
        # Try embedding-based retrieval
        from services import embedding_service
        q_emb = embedding_service.embed_text(question)
        sent_embs = [embedding_service.embed_text(s) for s in sentences]
        # cosine similarity
        import numpy as np
        sims = [np.dot(q_emb, s_emb) / (np.linalg.norm(q_emb) * (np.linalg.norm(s_emb) + 1e-12)) for s_emb in sent_embs]
        top_idx = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:top_k_sentences]
        answers = [sentences[i] for i in top_idx]
        return ' '.join(answers)
    except Exception:
        logger.debug("Embedding retrieval unavailable; falling back to keyword search", exc_info=True)
        # Fallback: keyword scoring
        q_words = [w.lower() for w in question.split() if len(w) > 3]
        scored = []
        for s in sentences:
            score = sum(1 for w in q_words if w in s.lower())
            scored.append((score, s))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = [s for sc, s in scored if sc > 0][:top_k_sentences]
        if top:
            return ' '.join(top)
        # last resort: return first 2 sentences
        return ' '.join(sentences[:2])
