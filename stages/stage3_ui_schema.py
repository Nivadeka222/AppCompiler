from schemas.models import (
    SystemDesignOutput,
    UISchema
)

from prompts.ui_schema import UI_SCHEMA_PROMPT

from utils.client import gemini
from utils.json_utils import safe_parse


def generate_ui_schema(
    design: SystemDesignOutput
) -> UISchema:

    response = gemini(
        model="unused",
        system=UI_SCHEMA_PROMPT,
        user=design.model_dump_json(indent=2),
    )

    data = safe_parse(response)

    return UISchema(**data)


if __name__ == "__main__":

    import json

    with open("design.json", "r", encoding="utf-8") as f:
        design = SystemDesignOutput(**json.load(f))

    ui_schema = generate_ui_schema(design)

    print(ui_schema.model_dump_json(indent=2))