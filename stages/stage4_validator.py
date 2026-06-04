from schemas.models import (
    DBSchema,
    APISchema,
    UISchema,
    AuthSchema,
    ValidationReport,
    ValidationError
)


def validate(
    db: DBSchema,
    api: APISchema,
    ui: UISchema,
    auth: AuthSchema
) -> ValidationReport:

    errors = []

    db_fields = set()

    for table in db.tables:
        for field in table.fields:
            db_fields.add(f"{table.name}.{field.name}")

    for endpoint in api.endpoints:

        for field in endpoint.request_fields:
            if field.source not in db_fields:
                errors.append(
                    ValidationError(
                        layer="api",
                        error_type="missing_db_field",
                        detail=f"{field.source} not found"
                    )
                )

        for field in endpoint.response_fields:
            if field.source not in db_fields:
                errors.append(
                    ValidationError(
                        layer="api",
                        error_type="missing_db_field",
                        detail=f"{field.source} not found"
                    )
                )

    auth_roles = {r.name for r in auth.roles}

    for page in ui.pages:

        for role in page.roles_allowed:
            if role not in auth_roles:
                errors.append(
                    ValidationError(
                        layer="ui",
                        error_type="unknown_role",
                        detail=f"{role} not found in auth schema"
                    )
                )

    return ValidationReport(
        passed=len(errors) == 0,
        errors=errors
    )
if __name__ == "__main__":

    import json

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

    report = validate(db, api, ui, auth)

    print(report.model_dump_json(indent=2))