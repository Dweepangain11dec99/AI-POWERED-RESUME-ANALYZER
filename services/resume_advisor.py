"""
Provide automated resume improvement suggestions.
Uses LLM if configured; otherwise uses heuristics.
"""
import logging
from typing import List

logger = logging.getLogger(__name__)


def suggest_improvements(resume_text: str, job_description: str | None = None) -> List[str]:
    """Return a list of recommendation strings.

    If an LLM is configured (`services.llm.call_llm`) it will be used to
    craft personalized suggestions. Otherwise a rule-based heuristic runs.
    """
    suggestions = []
    try:
        # Try LLM for rich suggestions
        from services.llm import call_llm
        prompt = "Provide 5 concise, actionable suggestions to improve this resume for the following job description:\n\nResume:\n" + (resume_text or '')
        if job_description:
            prompt += "\n\nJob Description:\n" + job_description
        prompt += "\n\nRespond as a JSON array of strings."
        resp = call_llm(prompt, max_tokens=300)
        # Try to parse JSON array
        import json
        try:
            parsed = json.loads(resp)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            # Fallback: split into lines
            lines = [l.strip('- \/n') for l in resp.split('\n') if l.strip()]
            return lines[:5]
    except NotImplementedError:
        logger.debug('LLM Gemini not implemented; falling back to heuristics')
    except Exception:
        logger.debug('LLM unavailable; using rule-based suggestions', exc_info=True)

    # Heuristic suggestions
    text = (resume_text or '').lower()
    if len(text) < 200:
        suggestions.append('Add a short summary paragraph that highlights your top skills and career goals.')
    if 'project' not in text:
        suggestions.append('Add 1-3 concrete projects with metrics (what you built and impact).')
    if 'year' not in text and 'years' not in text:
        suggestions.append('Clearly state years of experience for key skill areas.')
    if job_description and 'lead' in job_description.lower():
        suggestions.append('Emphasize leadership, mentoring, and cross-team collaboration experiences.')
    if 'certif' not in text and 'certificate' not in text:
        suggestions.append('List any relevant certifications or trainings that match the role.')

    # Fill up to 5 suggestions
    return suggestions[:5]
