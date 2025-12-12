"""Schemas module - All data structures for the application.

This module contains:
- internal_schemas: Pydantic models with rich validations (used in services)
- openai_schemas: JSON Schemas for OpenAI API responses (used in AI calls)
- enum_descriptions: Human-readable descriptions for all enums (used in prompts and reports)
"""

# Re-export from submodules for easier imports
from .internal_schemas import (
    ExecutiveSummarySchema,
    DetailedAnalysisSchema,
    ReportSchema,
    ReportGenerationResult,
    SuggestionGenerationResult,
)

from .openai_schemas import (
    REPORT_JSON_SCHEMA,
    SUGGESTION_JSON_SCHEMA,
    VALIDATION_JSON_SCHEMA,
)

from .enum_descriptions import (
    get_sdg_description,
    get_sdgs_with_descriptions,
    get_cognitive_processes_with_descriptions,
    get_enum_description,
    get_all_descriptions_for_prompt,
)

__all__ = [
    # Internal Pydantic Schemas
    "ExecutiveSummarySchema",
    "DetailedAnalysisSchema",
    "ReportSchema",
    "ReportGenerationResult",
    "SuggestionGenerationResult",
    # OpenAI JSON Schemas
    "REPORT_JSON_SCHEMA",
    "SUGGESTION_JSON_SCHEMA",
    "VALIDATION_JSON_SCHEMA",
    # Enum description helpers
    "get_sdg_description",
    "get_sdgs_with_descriptions",
    "get_cognitive_processes_with_descriptions",
    "get_enum_description",
    "get_all_descriptions_for_prompt",
]

