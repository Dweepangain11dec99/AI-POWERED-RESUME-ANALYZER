"""
LLM wrapper with support for OpenAI and a Gemini placeholder.
The wrapper is intentionally minimal: it reads environment variables and
calls OpenAI if `OPENAI_API_KEY` is set. If `GEMINI_API_KEY` is set the
Gemini.call() function is a stub that raises NotImplementedError so that
consumers know to implement their own Gemini integration.
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

_OPENAI_AVAILABLE = False
try:
    import openai
    _OPENAI_AVAILABLE = True
except Exception:
    openai = None


def call_llm(prompt: str, model: Optional[str] = None, max_tokens: int = 256) -> str:
    """Call a configured LLM and return text response.

    - If `OPENAI_API_KEY` set and openai package present, use that.
    - If `GEMINI_API_KEY` set, raise NotImplementedError (stub for Gemini integration).
    - Otherwise raise RuntimeError.
    """
    # Gemini integration (HTTP/REST): requires GEMINI_API_KEY and GEMINI_ENDPOINT
    gemini_key = os.getenv('GEMINI_API_KEY')
    gemini_endpoint = os.getenv('GEMINI_ENDPOINT')
    gemini_model = model or os.getenv('GEMINI_MODEL')
    if gemini_key:
        if not gemini_endpoint:
            raise NotImplementedError('GEMINI_API_KEY is set but GEMINI_ENDPOINT is not. Set GEMINI_ENDPOINT to the Gemini/PaLM REST URL.')

        payload = {
            'model': gemini_model or 'gemini-pro',
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': float(os.getenv('LLM_TEMPERATURE', '0.2'))
        }
        headers = {
            'Authorization': f'Bearer {gemini_key}',
            'Content-Type': 'application/json'
        }

        # Try httpx -> requests -> urllib
        resp_json = None
        status = None
        try:
            import httpx
            r = httpx.post(gemini_endpoint, json=payload, headers=headers, timeout=30.0)
            status = r.status_code
            resp_json = r.json()
        except Exception:
            try:
                import requests
                r = requests.post(gemini_endpoint, json=payload, headers=headers, timeout=30)
                status = r.status_code
                resp_json = r.json()
            except Exception:
                # Last-resort stdlib
                try:
                    import urllib.request, json
                    req = urllib.request.Request(gemini_endpoint, data=json.dumps(payload).encode('utf-8'), headers=headers)
                    with urllib.request.urlopen(req, timeout=30) as res:
                        status = res.getcode()
                        resp_json = json.loads(res.read().decode('utf-8'))
                except Exception as e:
                    logger.exception('Failed to call Gemini endpoint')
                    raise RuntimeError(f'Failed to call Gemini endpoint: {e}')

        if status is None or (status and status >= 400):
            raise RuntimeError(f'Gemini API error: status={status} body={resp_json}')

        # Robust parsing for potential Gemini/PaLM response shapes
        try:
            data = resp_json
            # common patterns: {'candidates': [...]}, {'output': ...}, {'text': '...'}, {'choices': [...]}
            if isinstance(data, dict):
                if 'candidates' in data and isinstance(data['candidates'], list):
                    parts = []
                    for c in data['candidates']:
                        if isinstance(c, dict):
                            # try common fields
                            for key in ('content', 'text', 'message', 'output'):
                                if key in c and c[key]:
                                    v = c[key]
                                    if isinstance(v, dict) and 'text' in v:
                                        parts.append(v['text'])
                                    else:
                                        parts.append(str(v))
                                    break
                    return '\n'.join(parts).strip()

                for key in ('text', 'output', 'response', 'content'):
                    if key in data and data[key]:
                        v = data[key]
                        if isinstance(v, str):
                            return v
                        if isinstance(v, dict) and 'text' in v:
                            return v['text']

                if 'choices' in data and isinstance(data['choices'], list) and data['choices']:
                    c0 = data['choices'][0]
                    if isinstance(c0, dict):
                        if 'message' in c0 and isinstance(c0['message'], dict) and 'content' in c0['message']:
                            return c0['message']['content']
                        if 'text' in c0:
                            return c0['text']

            # Fallback: stringify entire response
            return str(resp_json)
        except Exception:
            logger.exception('Failed to parse Gemini response')
            return str(resp_json)

    if os.getenv('OPENAI_API_KEY') and _OPENAI_AVAILABLE:
        try:
            openai.api_key = os.getenv('OPENAI_API_KEY')
            resp = openai.ChatCompletion.create(
                model=model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.2,
            )
            return resp.choices[0].message.content
        except Exception:
            logger.exception('OpenAI call failed')
            raise

    raise RuntimeError('No LLM backend configured (set OPENAI_API_KEY or GEMINI_API_KEY).')
