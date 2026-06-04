from schemas.models import ValidationReport
from utils.client import groq_call


REPAIR_PROMPT = """
You are a software architect.

Given validation errors and generated schemas,
return fixed JSON only.

Do not explain.
Return corrected JSON.
"""


def repair(
    report: ValidationReport,
    broken_json: str
) -> str:

    return groq_call(
        system=REPAIR_PROMPT,
        user=f"""
Validation Report:

{report.model_dump_json(indent=2)}

Broken JSON:

{broken_json}
"""
    )


if __name__ == "__main__":

    import json

    from stages.stage4_validator import validate

    from schemas.models import (
        DBSchema,
        APISchema,
        UISchema,
        AuthSchema
    )

    with open("db_schema.json") as f:
        db = DBSchema(**json.load(f))

    with open("api_schema.json") as f:
        api = APISchema(**json.load(f))

    with open("ui_schema.json") as f:
        ui = UISchema(**json.load(f))

    with open("auth_schema.json") as f:
        auth = AuthSchema(**json.load(f))

    report = validate(
        db,
        api,
        ui,
        auth
    )

    print(report.model_dump_json(indent=2))