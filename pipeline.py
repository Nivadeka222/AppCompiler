import json

from stages.stage1_intent import extract_intent
from stages.stage2_system_design import generate_system_design
from stages.stage3_db_schema import generate_db_schema
from stages.stage3_api_schema import generate_api_schema
from stages.stage3_ui_schema import generate_ui_schema
from stages.stage3_auth_schema import generate_auth_schema
from stages.stage4_validator import validate

from schemas.models import AppConfig


def run_pipeline(user_prompt: str):

    print("\n[1/7] Intent Extraction...")
    intent, metric = extract_intent(user_prompt)

    with open("intent.json", "w") as f:
        json.dump(
            intent.model_dump(),
            f,
            indent=2
        )

    print("[2/7] System Design...")
    design = generate_system_design(intent)

    with open("design.json", "w") as f:
        json.dump(
            design.model_dump(),
            f,
            indent=2
        )

    print("[3/7] Database Schema...")
    db_schema = generate_db_schema(design)

    with open("db_schema.json", "w") as f:
        json.dump(
            db_schema.model_dump(),
            f,
            indent=2
        )

    print("[4/7] API Schema...")
    api_schema = generate_api_schema(design)

    with open("api_schema.json", "w") as f:
        json.dump(
            api_schema.model_dump(),
            f,
            indent=2
        )

    print("[5/7] UI Schema...")
    ui_schema = generate_ui_schema(design)

    with open("ui_schema.json", "w") as f:
        json.dump(
            ui_schema.model_dump(),
            f,
            indent=2
        )

    print("[6/7] Auth Schema...")
    auth_schema = generate_auth_schema(design)

    with open("auth_schema.json", "w") as f:
        json.dump(
            auth_schema.model_dump(),
            f,
            indent=2
        )

    print("[7/7] Validation...")
    report = validate(
        db_schema,
        api_schema,
        ui_schema,
        auth_schema
    )

    print(report.model_dump_json(indent=2))

    app_config = AppConfig(
        intent=intent,
        system_design=design,
        db_schema=db_schema,
        api_schema=api_schema,
        ui_schema=ui_schema,
        auth_schema=auth_schema
    )

    with open("app_config.json", "w") as f:
        json.dump(
            app_config.model_dump(),
            f,
            indent=2
        )

    return app_config


if __name__ == "__main__":

    prompt = input("\nEnter app idea:\n> ")

    result = run_pipeline(prompt)

    print("\nPipeline Complete")
    print(result.model_dump_json(indent=2))