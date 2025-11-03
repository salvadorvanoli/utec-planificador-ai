from fastapi import APIRouter, HTTPException
from app.api.schemas.planificacion_dto import PlanificacionRequestDTO
from app.api.schemas.suggestion_dto import SuggestionResponse
from app.service.suggestion_service import generate_suggestions

router = APIRouter()

@router.post("/suggestions", response_model=SuggestionResponse)
async def get_suggestions(body: PlanificacionRequestDTO):
    if not body or not body.planificacionDocente:
        raise HTTPException(status_code=400, detail="La planificación docente es requerida")

    # Convertir a dict para procesar
    planificacion_dict = body.planificacionDocente.model_dump()

    result = generate_suggestions(
        planificacion_dict,
        context={"course_id": body.course_id}
    )

    return SuggestionResponse(
        analysis=result.get('analysis', ''),
        pedagogical_suggestions=result.get('pedagogical_suggestions', '')
    )
