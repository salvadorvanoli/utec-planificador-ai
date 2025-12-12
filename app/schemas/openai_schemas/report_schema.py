"""OpenAI JSON Schema for pedagogical report generation."""

REPORT_JSON_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "pedagogical_report",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Mensaje personalizado sobre el estado general del curso"
                },
                "strengths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de 3-5 aspectos positivos específicos"
                },
                "improvementAreas": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de 2-4 áreas que necesitan fortalecimiento"
                },
                "recommendations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de 4-8 recomendaciones específicas y accionables"
                },
                "detailedAnalysis": {
                    "type": "object",
                    "properties": {
                        "cognitiveProcesses": {
                            "type": "string",
                            "description": "Análisis cualitativo de la distribución y balance"
                        },
                        "transversalCompetencies": {
                            "type": "string",
                            "description": "Análisis de la diversidad y balance"
                        },
                        "modalityBalance": {
                            "type": "string",
                            "description": "Evaluación del equilibrio de modalidades"
                        },
                        "teachingStrategies": {
                            "type": "string",
                            "description": "Análisis de la variedad metodológica"
                        },
                        "resources": {
                            "type": "string",
                            "description": "Evaluación de la diversidad de materiales"
                        },
                        "sdgLinkage": {
                            "type": "string",
                            "description": "Análisis del compromiso con el desarrollo sostenible"
                        }
                    },
                    "required": [
                        "cognitiveProcesses",
                        "transversalCompetencies",
                        "modalityBalance",
                        "teachingStrategies",
                        "resources",
                        "sdgLinkage"
                    ],
                    "additionalProperties": False
                }
            },
            "required": [
                "message",
                "strengths",
                "improvementAreas",
                "recommendations",
                "detailedAnalysis"
            ],
            "additionalProperties": False
        }
    }
}

