from fastapi import APIRouter, HTTPException
from app.api.schemas.report_dto import ReportRequest, ReportResponse
from app.service.report_service import generate_basic_report

router = APIRouter()

@router.post("/report/generate", response_model=ReportResponse)
async def generate_report(body: ReportRequest):
    if not body or not body.estadisticas:
        raise HTTPException(status_code=400, detail="Las estadísticas del curso son requeridas")

    # Convertir estadísticas a dict
    estadisticas_dict = body.estadisticas.model_dump()

    result = generate_basic_report(body.course_id, estadisticas_dict)

    return ReportResponse(
        success=result.get('success', True),
        reporte=result.get('reporte', {}),
        recomendaciones=result.get('recomendaciones', []),
        calificacion_general=result.get('calificacion_general', '')
    )
