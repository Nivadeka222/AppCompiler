"""
Shared LLM clients.
Gemini  → generation stages
Groq    → repair stage
"""

import os
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


# ── Gemini ─────────────────────────────

gemini_client = genai.Client(
    api_key=_require_env("GEMINI_API_KEY")
)

GEMINI_FLASH = "llama-3.3-70b-versatile"
GEMINI_PRO = "llama-3.3-70b-versatile"


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
    )


# ── Groq ───────────────────────────────

groq_client = Groq(
    api_key=_require_env("GROQ_API_KEY")
)

GROQ_MODEL = "llama-3.3-70b-versatile"


def groq_call(
    system: str,
    user: str,
    temperature: float = 0.1,
) -> str:

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    return response.choices[0].message.content.strip()