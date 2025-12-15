"""Report API endpoints."""
import logging
from fastapi import APIRouter, HTTPException
from app.api.v2.dtos import ReportRequest, ReportResponse
from app.services.report_service import ReportService

router = APIRouter(tags=["Reports"])
logger = logging.getLogger(__name__)

report_service = ReportService()


@router.post("/report/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate a pedagogical evaluation report.
    """
    try:
        statistics_dict = request.statistics.model_dump()
        planning_dict = request.coursePlanning.model_dump()

        result = report_service.generate_report(
            course_id=request.courseId,
            statistics=statistics_dict,
            planning=planning_dict
        )

        return ReportResponse(
            success=result.success,
            report=result.report.model_dump(),
            recommendations=result.recommendations,
            overallRating=""
        )

    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error generating report. Please try again later."
        )


