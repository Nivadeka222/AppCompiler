"""
Shared LLM clients.
Gemini -> generation stages
Groq -> generation + repair
"""

import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from groq import Groq

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


# ==================================================
# Retry callback hook (set by pipeline.py)
# ==================================================

_current_stage: str = ""
_retry_callback = None  # callable(stage: str, attempt: int) | None


# ==================================================
# Gemini (unused now, routed to Groq)
# ==================================================

gemini_client = genai.Client(
    api_key=_require_env("GEMINI_API_KEY")
)

GEMINI_FLASH = "llama-3.1-8b-instant"
GEMINI_PRO = "llama-3.1-8b-instant"


def gemini(
    model: str,
    system: str,
    user: str,
    temperature: float = 0.2,
) -> str:
    return groq_call(
        system=system,
        user=user,
        temperature=temperature,
        max_tokens=2500,
    )


# ==================================================
# Groq
# ==================================================

groq_client = Groq(
    api_key=_require_env("GROQ_API_KEY")
)

GROQ_MODEL = "llama-3.1-8b-instant"


def groq_call(
    system: str,
    user: str,
    temperature: float = 0.1,
    max_tokens: int = 2500,
) -> str:

    print("\n" + "=" * 60)
    print("SYSTEM LENGTH:", len(system))
    print("USER LENGTH:", len(user))
    print("MAX TOKENS:", max_tokens)
    print("=" * 60 + "\n")

    for attempt in range(4):
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "rate_limit_exceeded" in str(e) and attempt < 3:
                wait = 15 * (attempt + 1)
                print(f"Rate limit hit, retrying in {wait}s... (attempt {attempt + 1}/4)")
                if _retry_callback is not None:
                    try:
                        _retry_callback(_current_stage, attempt + 1)
                    except Exception:
                        pass
                time.sleep(wait)
            else:
                raise