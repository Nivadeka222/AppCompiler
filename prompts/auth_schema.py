AUTH_SCHEMA_PROMPT = """
Generate authentication and authorization schema.

Return JSON only.

{
  "strategy": "jwt",
  "token_expiry_seconds": 86400,
  "roles": [
    {
      "name": "Admin",
      "permissions": [
        {
          "resource": "contacts",
          "actions": ["create","read","update","delete"]
        }
      ],
      "can_access_pages": ["/dashboard"]
    }
  ],
  "public_routes": ["/login","/register"]
}
"""