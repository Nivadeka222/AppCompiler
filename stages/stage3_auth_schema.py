from schemas.models import (
    SystemDesignOutput,
    AuthSchema
)


def generate_auth_schema(
    design: SystemDesignOutput
) -> AuthSchema:

    admin_pages = []
    user_pages = []

    for page in design.pages:

        roles = getattr(page, "access_roles", [])

        roles_lower = [r.lower() for r in roles]

        if "admin" in roles_lower:
            admin_pages.append(page.path)

        if "user" in roles_lower:
            user_pages.append(page.path)

    data = {
        "strategy": "jwt",
        "token_expiry_seconds": 86400,
        "roles": [
            {
                "name": "Admin",
                "permissions": [
                    {
                        "resource": "*",
                        "actions": [
                            "create",
                            "read",
                            "update",
                            "delete"
                        ]
                    }
                ],
                "can_access_pages": admin_pages
            },
            {
                "name": "User",
                "permissions": [
                    {
                        "resource": "*",
                        "actions": [
                            "read"
                        ]
                    }
                ],
                "can_access_pages": user_pages
            }
        ],
        "public_routes": [
            "/login",
            "/register"
        ]
    }

    return AuthSchema(**data)


if __name__ == "__main__":

    import json

    with open("design.json", "r", encoding="utf-8") as f:
        design = SystemDesignOutput(**json.load(f))

    auth_schema = generate_auth_schema(design)

    print(auth_schema.model_dump_json(indent=2))