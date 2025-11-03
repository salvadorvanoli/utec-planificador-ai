from pydantic import BaseModel
from typing import Dict, List

class CourseStatisticsDTO(BaseModel):
    """Statistics extracted from a course planning for analysis"""
    cognitiveProcesses: Dict[str, int] = {}  # e.g., {"REMEMBER": 10, "UNDERSTAND": 25}
    transversalCompetencies: Dict[str, int] = {}
    learningModalities: Dict[str, int] = {}
    teachingStrategies: Dict[str, int] = {}
    mostUsedResources: List[str] = []
    linkedSDGs: Dict[str, int] = {}
    averageActivityDurationInMinutes: int = 0
    totalWeeks: int = 0
    totalInPersonHours: int = 0
    totalVirtualHours: int = 0
    totalHybridHours: int = 0

class ReportRequest(BaseModel):
    courseId: str
    statistics: CourseStatisticsDTO

class ReportResponse(BaseModel):
    success: bool = True
    report: Dict = {}
    recommendations: List[str] = []
    overallRating: str = ""

