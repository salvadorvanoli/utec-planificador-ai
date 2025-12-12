"""OpenAI JSON Schemas for structured outputs."""
from .report_schema import REPORT_JSON_SCHEMA
from .suggestion_schema import SUGGESTION_JSON_SCHEMA
from .validation_schema import VALIDATION_JSON_SCHEMA

__all__ = [
    "REPORT_JSON_SCHEMA",
    "SUGGESTION_JSON_SCHEMA",
    "VALIDATION_JSON_SCHEMA",
]

