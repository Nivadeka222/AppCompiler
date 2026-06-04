DB_SCHEMA_PROMPT = """
You are a senior database architect.

Convert the system design JSON into a relational database schema.

Rules:
- Use snake_case table names
- Add primary keys
- Add foreign keys from relationships
- Infer SQL-like types
- Return JSON only

{
  "tables": [
    {
      "name": "",
      "fields": [
        {
          "name": "",
          "type": "",
          "required": true,
          "unique": false,
          "default": null,
          "references": null
        }
      ],
      "indexes": []
    }
  ]
}
"""