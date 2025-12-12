"""Internal Pydantic internal_schemas for data validation."""
from .report_schemas import (
    ExecutiveSummarySchema,
    DetailedAnalysisSchema,
    ReportSchema,
    ReportGenerationResult,
)
from .suggestion_schemas import SuggestionGenerationResult

__all__ = [
    "ExecutiveSummarySchema",
    "DetailedAnalysisSchema",
    "ReportSchema",
    "ReportGenerationResult",
    "SuggestionGenerationResult",
]

