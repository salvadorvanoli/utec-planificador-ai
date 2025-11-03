from fastapi import APIRouter, HTTPException
from app.api.schemas.report_dto import ReportRequest, ReportResponse
from app.service.report_service import generate_basic_report

router = APIRouter()

@router.post("/report/generate", response_model=ReportResponse)
async def generate_report(body: ReportRequest):
    if not body or not body.statistics:
        raise HTTPException(status_code=400, detail="Course statistics are required")

    # Convert statistics to dict
    statistics_dict = body.statistics.model_dump()

    result = generate_basic_report(body.courseId, statistics_dict)

    return ReportResponse(
        success=result.get('success', True),
        report=result.get('report', {}),
        recommendations=result.get('recommendations', []),
        overallRating=result.get('overallRating', '')
    )

