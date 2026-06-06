import json
import time
from typing import Generator

from stages.stage1_intent import extract_intent
from stages.stage2_system_design import generate_system_design
from stages.stage3_db_schema import generate_db_schema
from stages.stage3_api_schema import generate_api_schema
from stages.stage3_ui_schema import generate_ui_schema
from stages.stage3_auth_schema import generate_auth_schema
from stages.stage4_validator import validate
from schemas.models import AppConfig
import utils.client as groq_client

STAGES = [
    "Intent Extraction",
    "System Design",
    "Database Schema",
    "API Schema",
    "UI Schema",
    "Auth Schema",
    "Validation",
]

def run_pipeline_stream(user_prompt: str) -> Generator:
    # Collect retry events emitted by groq_client during blocking calls
    retry_events: list[dict] = []
    groq_client._retry_callback = lambda stage, attempt: retry_events.append(
        {"stage": stage, "attempt": attempt}
    )

    def flush():
        while retry_events:
            yield ("__retry__", retry_events.pop(0))

    groq_client._current_stage = "Intent Extraction"
    yield ("Intent Extraction", None)
    intent, _ = extract_intent(user_prompt)
    yield from flush()
    with open("intent.json", "w") as f:
        json.dump(intent.model_dump(), f, indent=2)
    time.sleep(5)

    groq_client._current_stage = "System Design"
    yield ("System Design", None)
    design = generate_system_design(intent)
    yield from flush()
    with open("design.json", "w") as f:
        json.dump(design.model_dump(), f, indent=2)
    time.sleep(5)

    groq_client._current_stage = "Database Schema"
    yield ("Database Schema", None)
    db_schema = generate_db_schema(design)
    yield from flush()
    with open("db_schema.json", "w") as f:
        json.dump(db_schema.model_dump(), f, indent=2)
    time.sleep(5)

    groq_client._current_stage = "API Schema"
    yield ("API Schema", None)
    api_schema = generate_api_schema(design)
    yield from flush()
    with open("api_schema.json", "w") as f:
        json.dump(api_schema.model_dump(), f, indent=2)
    time.sleep(5)

    groq_client._current_stage = "UI Schema"
    yield ("UI Schema", None)
    ui_schema = generate_ui_schema(design)
    yield from flush()
    with open("ui_schema.json", "w") as f:
        json.dump(ui_schema.model_dump(), f, indent=2)
    time.sleep(5)

    groq_client._current_stage = "Auth Schema"
    yield ("Auth Schema", None)
    auth_schema = generate_auth_schema(design)
    yield from flush()
    with open("auth_schema.json", "w") as f:
        json.dump(auth_schema.model_dump(), f, indent=2)

    groq_client._current_stage = "Validation"
    yield ("Validation", None)
    validate(db_schema, api_schema, ui_schema, auth_schema)

    app_config = AppConfig(
        intent=intent,
        system_design=design,
        db_schema=db_schema,
        api_schema=api_schema,
        ui_schema=ui_schema,
        auth_schema=auth_schema,
    )
    with open("app_config.json", "w") as f:
        json.dump(app_config.model_dump(), f, indent=2)

    yield ("Complete", app_config)


def run_pipeline(user_prompt: str):
    result = None
    for _, r in run_pipeline_stream(user_prompt):
        if r is not None:
            result = r
    return result


if __name__ == "__main__":
    prompt = input("\nEnter app idea:\n> ")
    result = run_pipeline(prompt)
    print("\nPipeline Complete")
    print(result.model_dump_json(indent=2))