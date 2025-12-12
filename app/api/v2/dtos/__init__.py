"""API DTOs (Data Transfer Objects) for HTTP requests/responses."""
from .chat_dto import ChatRequest
from .planification_dto import CoursePlanningRequestDTO, CoursePlanningDTO
from .suggestion_dto import SuggestionResponse
from .report_dto import CourseStatisticsDTO, ReportRequest, ReportResponse

__all__ = [
    "ChatRequest",
    "CoursePlanningRequestDTO",
    "CoursePlanningDTO",
    "CourseStatisticsDTO",
    "ReportRequest",
    "ReportResponse",
    "SuggestionResponse",
]

