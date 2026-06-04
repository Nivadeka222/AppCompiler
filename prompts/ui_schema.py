UI_SCHEMA_PROMPT = """
You are a senior frontend architect.

Generate ONLY valid JSON.

{
  "pages": [
    {
      "name": "Contacts",
      "path": "/contacts",
      "roles_allowed": ["User"],
      "components": [
        {
          "id": "contacts_table",
          "type": "table",
          "title": "Contacts",
          "fields": [],
          "data_source": "/api/v1/contacts",
          "roles_visible": ["User"]
        }
      ],
      "layout": "default"
    }
  ],
  "nav_items": []
}
"""