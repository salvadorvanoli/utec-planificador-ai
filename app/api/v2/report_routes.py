"""Report API endpoints."""
import logging
from fastapi import APIRouter, HTTPException
from app.api.schemas.report_dto import ReportRequest, ReportResponse
from app.services.report_service import ReportService

router = APIRouter(tags=["Reports"])
logger = logging.getLogger(__name__)

# Service instance
report_service = ReportService()


@router.post("/report/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate a pedagogical evaluation report.

    Args:
        request: Report request with course statistics and planning

    Returns:
        Report with analysis, strengths, areas for improvement, and recommendations
    """
    try:
        # Convert DTOs to dictionaries
        statistics_dict = request.statistics.model_dump()
        planning_dict = request.coursePlanning.model_dump()

        # Generate report (returns ReportGenerationResult schema)
        result = report_service.generate_report(
            course_id=request.courseId,
            statistics=statistics_dict,
            planning=planning_dict
        )

        # Convert Pydantic models to dicts for response
        return ReportResponse(
            success=result.success,
            report=result.report.model_dump(),  # Serialize Pydantic model to dict
            recommendations=result.recommendations,
            overallRating=""  # No longer used but kept for backwards compatibility
        )

    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error generating report. Please try again later."
        )


