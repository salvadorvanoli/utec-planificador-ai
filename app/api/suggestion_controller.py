from fastapi import APIRouter, HTTPException
from app.api.schemas.planification_dto import CoursePlanningRequestDTO
from app.api.schemas.suggestion_dto import SuggestionResponse
from app.service.suggestion_service import generate_suggestions

router = APIRouter()

@router.post("/suggestions", response_model=SuggestionResponse)
async def get_suggestions(body: CoursePlanningRequestDTO):
    if not body or not body.coursePlanning:
        raise HTTPException(status_code=400, detail="Course planning is required")

    # Convert to dict for processing
    planning_dict = body.coursePlanning.model_dump()

    result = generate_suggestions(
        planning_dict,
        context={"course_id": body.coursePlanning.id}
    )

    return SuggestionResponse(
        analysis=result.get('analysis', ''),
        pedagogicalSuggestions=result.get('pedagogicalSuggestions', '')
    )

