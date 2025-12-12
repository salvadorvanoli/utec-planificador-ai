"""OpenAI JSON Schema for pedagogical suggestions generation."""

SUGGESTION_JSON_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "pedagogical_suggestions",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "analysis": {
                    "type": "string",
                    "description": "Evaluación holística detallada de la planificación (2-3 párrafos)"
                },
                "pedagogicalSuggestions": {
                    "type": "string",
                    "description": "Lista numerada de 5-7 sugerencias específicas y accionables"
                }
            },
            "required": ["analysis", "pedagogicalSuggestions"],
            "additionalProperties": False
        }
    }
}

