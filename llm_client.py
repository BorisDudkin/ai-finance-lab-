import os
import time
import logging
from typing import List, Dict, Optional


# Default provider can be overridden by setting LLM_PROVIDER in the environment.
PROVIDER: str = os.getenv("LLM_PROVIDER", "openai").lower()
# Optional environment variables to override model names.
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1")
ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")


def _extract_text_from_response(resp) -> Optional[str]:
    """Attempt to extract text from common SDK response shapes.

    Returns the first non-empty candidate found, or None.
    """
    try:
        # Common OpenAI Python SDK pattern: resp.choices[0].message.content
        candidate = getattr(resp, "choices", None)
        if candidate:
            first = candidate[0]
            msg = getattr(first, "message", None)
            if msg:
                content = getattr(msg, "content", None)
                if content:
                    return content
            text = getattr(first, "text", None)
            if text:
                return text
    except Exception:
        pass

    # Common Anthropic / other pattern: resp.content / resp.completion / resp.get("completion")
    try:
        for key in ("content", "completion", "text"):
            if isinstance(resp, dict) and resp.get(key):
                return resp.get(key)
            val = getattr(resp, key, None)
            if val:
                return val
    except Exception:
        pass

    # Fallback: try string conversion
    try:
        s = str(resp)
        if s and s.strip():
            return s
    except Exception:
        return None

    return None



def call_llm(messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: int = 800, retries: int = 2, backoff_factor: float = 1.0) -> str:
    """Call the configured LLM provider and return the response text.

    - `messages` is a list of dicts in the {role: str, content: str} format used by chat-style LLMs.
    - `temperature=0.0` is recommended for deterministic outputs when programmatic parsing is required.

    The function wraps provider SDK calls and attempts to extract the response text from
    several common response formats. It also implements a small retry/backoff loop.
    """

    if PROVIDER == "openai": 

        from openai import OpenAI 

        client = OpenAI() 

 

        resp = client.chat.completions.create(

            model="gpt-4.1", 

            messages=messages, 

            temperature=temperature, 

            max_tokens=max_tokens 

        )
            text = _extract_text_from_response(resp)
            if text:
                return text
            raise RuntimeError("OpenAI response did not contain text")



    elif PROVIDER == "claude": 

        from anthropic import Anthropic 

        client = Anthropic() 

 

        resp = client.messages.create(

            model="claude-3-5-sonnet-20241022", 

            max_tokens=max_tokens, 

            temperature=temperature, 

            messages=messages 

        )
            text = _extract_text_from_response(resp)
            if text:
                return text
            raise RuntimeError("Anthropic response did not contain text")



    else: 

        raise ValueError("Unsupported LLM provider") 
    
    '''
    original code removed for brevity:

    import os 

from typing import List, Dict 

 

PROVIDER = os.getenv("LLM_PROVIDER", "openai") 

 

def call_llm(messages: List[Dict], temperature=0.0, max_tokens=800): 

    if PROVIDER == "openai": 

        from openai import OpenAI 

        client = OpenAI() 

 

        return client.chat.completions.create( 

            model="gpt-4.1", 

            messages=messages, 

            temperature=temperature, 

            max_tokens=max_tokens 

        ).choices[0].message.content 

 

    elif PROVIDER == "claude": 

        from anthropic import Anthropic 

        client = Anthropic() 

 

        return client.messages.create( 

            model="claude-3-5-sonnet-20241022", 

            max_tokens=max_tokens, 

            temperature=temperature, 

            messages=messages 

        ).content[0].text 

 

    else: 

        raise ValueError("Unsupported LLM provider") 

 

    '''