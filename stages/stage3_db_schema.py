from schemas.models import (
    SystemDesignOutput,
    DBSchema
)

from prompts.db_schema import DB_SCHEMA_PROMPT
from utils.client import gemini, GEMINI_PRO
from utils.json_utils import safe_parse


def generate_db_schema(
    design: SystemDesignOutput
) -> DBSchema:

    response = gemini(
        model=GEMINI_PRO,
        system=DB_SCHEMA_PROMPT,
        user=design.model_dump_json(indent=2),
    )

    print("\n" + "=" * 80)
    print("RAW DB SCHEMA OUTPUT")
    print("=" * 80)
    print(response)
    print("=" * 80 + "\n")
    print(response)
    data = safe_parse(response)

    return DBSchema(**data)


if __name__ == "__main__":

    from stages.stage1_intent import extract_intent
    from stages.stage2_system_design import generate_system_design

    test_prompt = """
    Build a CRM application with login, contacts, dashboard,
    role-based access, and premium plan with payments.
    Admins can see analytics.
    """

    intent, metric = extract_intent(test_prompt)

    design = generate_system_design(intent)

    with open("design.json", "w", encoding="utf-8") as f:
        f.write(design.model_dump_json(indent=2))

    db_schema = generate_db_schema(design)

    print("\nStage 3A: Database Schema")
    print("=" * 50)
    print(db_schema.model_dump_json(indent=2))