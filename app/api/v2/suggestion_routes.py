"""Suggestion API endpoints."""
import logging
from fastapi import APIRouter, HTTPException
from app.api.schemas.planification_dto import CoursePlanningRequestDTO
from app.api.schemas.suggestion_dto import SuggestionResponse
from app.services.suggestion_service import SuggestionService

router = APIRouter(tags=["Suggestions"])
logger = logging.getLogger(__name__)

# Service instance
suggestion_service = SuggestionService()


@router.post("/suggestions", response_model=SuggestionResponse)
async def generate_suggestions(request: CoursePlanningRequestDTO):
    """
    Generate pedagogical suggestions for a course planning.

    Args:
        request: Course planning data

    Returns:
        Analysis and pedagogical suggestions
    """
    try:
        # Extract planning data
        planning_dict = request.coursePlanning.model_dump()

        # Generate suggestions (returns SuggestionGenerationResult schema)
        result = suggestion_service.generate_suggestions(planning_dict)

        # Schema already guarantees correct structure, just return it
        return SuggestionResponse(
            analysis=result.analysis,
            pedagogicalSuggestions=result.pedagogicalSuggestions
        )

    except Exception as e:
        logger.error(f"Error generating suggestions: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error generating suggestions. Please try again later."
        )


