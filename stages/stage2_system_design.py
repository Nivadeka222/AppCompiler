import json

from schemas.models import (
    IntentOutput,
    SystemDesignOutput
)

from prompts.system_design import (
    SYSTEM_DESIGN_PROMPT
)

from utils.client import gemini, GEMINI_FLASH
from utils.json_utils import safe_parse


def generate_system_design(
    intent: IntentOutput
) -> SystemDesignOutput:

    prompt = f"""
Intent JSON:

{intent.model_dump_json(indent=2)}
"""

    response = gemini(
        model=GEMINI_FLASH,
        system=SYSTEM_DESIGN_PROMPT,
        user=prompt,
    )

    data = safe_parse(response)

    return SystemDesignOutput(**data)
if __name__ == "__main__":

    with open("intent.json", "r", encoding="utf-8") as f:
        intent = IntentOutput.model_validate_json(f.read())

    design = generate_system_design(intent)

    print(design.model_dump_json(indent=2))