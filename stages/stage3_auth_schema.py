from schemas.models import (
    SystemDesignOutput,
    AuthSchema
)

from prompts.auth_schema import AUTH_SCHEMA_PROMPT

from utils.client import gemini, GEMINI_FLASH
from utils.json_utils import safe_parse


def generate_auth_schema(
    design: SystemDesignOutput
) -> AuthSchema:

    response = gemini(
        model=GEMINI_FLASH,
        system=AUTH_SCHEMA_PROMPT,
        user=design.model_dump_json(indent=2)
    )

    data = safe_parse(response)

    return AuthSchema(**data)


if __name__ == "__main__":

    import json

    from schemas.models import SystemDesignOutput

    with open("design.json", "r") as f:
        design = SystemDesignOutput(**json.load(f))

    auth_schema = generate_auth_schema(design)

    print(auth_schema.model_dump_json(indent=2))