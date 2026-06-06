"""
Stage 1 — Intent Extraction
Raw user prompt → structured IntentOutput
Model: Gemini 1.5 Flash (cheap, fast, JSON mode)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.client import gemini, groq_call, GEMINI_FLASH, GROQ_MODEL
from utils.json_utils import safe_parse
from utils.logger import StageMetric, Timer
from schemas.models import IntentOutput
from pydantic import ValidationError

SYSTEM_PROMPT = """You are Stage 1 of an application compiler: Intent Extraction.

Parse the user's app description into structured JSON.

Rules:
- Extract ALL entities (users, products, orders, contacts, etc.)
- Infer roles even if implicit ("admin sees analytics" → roles: admin, user)
- Every feature must list which roles can access it
- If prompt is vague, make a reasonable assumption and add it to "assumptions"
- Output ONLY valid JSON. No markdown. No explanation.

Required JSON structure:
{
  "app_name": "string",
  "app_type": "string",
  "entities": [{"name": "str", "description": "str", "attributes": ["str"]}],
  "roles": [{"name": "str", "permissions": ["str"]}],
  "features": [{"name": "str", "description": "str", "requires_auth": bool, "roles_allowed": ["str"]}],
  "integrations": ["str"],
  "assumptions": ["str"]
}"""

REPAIR_SYSTEM = """You are a JSON repair specialist.
You will receive broken JSON and an error message.
Fix ONLY the structure. Keep all content identical.
Output ONLY valid JSON. No markdown. No explanation."""


def extract_intent(user_prompt: str) -> tuple[IntentOutput, StageMetric]:
    retries = 0
    raw = ""

    with Timer() as t:
        try:
            raw = gemini(
                model=GEMINI_FLASH,
                system=SYSTEM_PROMPT,
                user=f"Extract intent from:\n\n{user_prompt}"
            )

            data = safe_parse(raw)
            result = IntentOutput(**data)

        except (ValueError, ValidationError) as e:

            retries = 1
            print(f"  [Stage 1] repair triggered: {e}")

            repair_user = f"""
Original prompt:
{user_prompt}

Broken output:
{raw[:1000]}

Fix and return valid JSON only.
"""

            try:
                raw = groq_call(
                    system=REPAIR_SYSTEM,
                    user=repair_user
                )

                data = safe_parse(raw)
                result = IntentOutput(**data)

            except Exception as e2:

                metric = StageMetric(
                    stage="intent",
                    model=GEMINI_FLASH,
                    success=False,
                    retries=retries,
                    latency_ms=t.elapsed_ms,
                    error=str(e2)
                )

                raise ValueError(
                    f"Stage 1 failed after repair: {e2}"
                ) from e2

    metric = StageMetric(
        stage="intent",
        model=GEMINI_FLASH,
        success=True,
        retries=retries,
        latency_ms=t.elapsed_ms
    )

    return result, metric


if __name__ == "__main__":
    prompt = (
        "Build a CRM with login, contacts, dashboard, "
        "role-based access, and premium plan with payments. "
        "Admins can see analytics."
    )
    print("Stage 1: Intent Extraction\n" + "="*50)
    intent, metric = extract_intent(prompt)
    print(intent.model_dump_json(indent=2))
    print(f"\nMetrics: {metric}")
