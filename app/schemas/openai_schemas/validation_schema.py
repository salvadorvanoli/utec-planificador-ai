"""OpenAI JSON Schema for input validation (educational relevance)."""

VALIDATION_JSON_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "input_validation",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "is_valid": {
                    "type": "boolean",
                    "description": "True si la consulta es educativamente relevante, False si no lo es"
                },
                "reason": {
                    "type": "string",
                    "description": "Breve explicación de por qué la consulta es o no válida"
                }
            },
            "required": ["is_valid", "reason"],
            "additionalProperties": False
        }
    }
}

