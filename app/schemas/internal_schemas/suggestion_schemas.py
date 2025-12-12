"""Response internal_schemas for suggestion generation."""
from pydantic import BaseModel, Field


class SuggestionGenerationResult(BaseModel):
    """Result of suggestion generation with normalized structure."""
    analysis: str = Field(
        description="Detailed pedagogical analysis of the planning (2-3 paragraphs)",
        min_length=1
    )
    pedagogicalSuggestions: str = Field(
        description="Numbered list of 5-8 specific and actionable suggestions",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "analysis": "El curso presenta una estructura sólida con 16 semanas...",
                "pedagogicalSuggestions": "1. Incorporar más actividades de nivel CREAR\n2. Diversificar competencias..."
            }
        }

