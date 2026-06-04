API_SCHEMA_PROMPT = """
You are a backend architect.

Generate ONLY valid JSON.

Output format:

{
  "base_path": "/api/v1",
  "endpoints": [
    {
      "path": "/contacts",
      "method": "GET",
      "summary": "List contacts",
      "roles_allowed": ["User"],
      "request_fields": [],
      "response_fields": [
        {
          "name": "id",
          "type": "integer",
          "source": "contacts.id"
        }
      ],
      "auth_required": true
    }
  ]
}
"""