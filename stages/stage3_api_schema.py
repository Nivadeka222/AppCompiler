from schemas.models import (
    SystemDesignOutput,
    APISchema
)

from prompts.api_schema import API_SCHEMA_PROMPT

from utils.client import gemini
from utils.json_utils import safe_parse


def generate_api_schema(
    design: SystemDesignOutput
) -> APISchema:

    prompt = f"""
{design.model_dump_json(indent=2)}
"""

    response = gemini(
        model="unused",
        system=API_SCHEMA_PROMPT,
        user=prompt,
    )
    print(response)

    data = safe_parse(response)

    return APISchema(**data)


if __name__ == "__main__":

    import json

    with open("design.json", "r", encoding="utf-8") as f:
        design = SystemDesignOutput(**json.load(f))

    api_schema = generate_api_schema(design)

    print(api_schema.model_dump_json(indent=2))