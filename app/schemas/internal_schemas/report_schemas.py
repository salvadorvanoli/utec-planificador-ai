"""Response internal_schemas for report generation."""
from pydantic import BaseModel, Field
from typing import List


class ExecutiveSummarySchema(BaseModel):
    """Executive summary of course statistics."""
    totalWeeks: int = Field(default=0, description="Total number of weeks in the course")
    totalHours: int = Field(default=0, description="Total hours (in-person + virtual + hybrid)")
    inPersonHours: int = Field(default=0, description="In-person hours")
    virtualHours: int = Field(default=0, description="Virtual hours")
    hybridHours: int = Field(default=0, description="Hybrid hours")
    averageActivityDuration: str = Field(default="0 min", description="Average activity duration")
    totalActivitiesAnalyzed: int = Field(default=0, description="Total number of activities analyzed")


class DetailedAnalysisSchema(BaseModel):
    """Detailed qualitative analysis of pedagogical aspects."""
    cognitiveProcesses: str = Field(default="", description="Analysis of cognitive processes (Bloom)")
    transversalCompetencies: str = Field(default="", description="Analysis of transversal competencies")
    modalityBalance: str = Field(default="", description="Evaluation of learning modality balance")
    teachingStrategies: str = Field(default="", description="Analysis of teaching strategies")
    resources: str = Field(default="", description="Evaluation of learning resources")
    sdgLinkage: str = Field(default="", description="Analysis of SDG linkage")


class ReportSchema(BaseModel):
    """Complete pedagogical evaluation report."""
    courseId: str = Field(description="Course identifier")
    analysisDate: str = Field(description="Date of analysis (YYYY-MM-DD)")
    message: str = Field(description="Summary message about the course")
    executiveSummary: ExecutiveSummarySchema = Field(description="Executive summary with key metrics")
    detailedAnalysis: DetailedAnalysisSchema = Field(description="Detailed qualitative analysis")
    strengths: List[str] = Field(default_factory=list, description="List of course strengths")
    improvementAreas: List[str] = Field(default_factory=list, description="Areas for improvement")


class ReportGenerationResult(BaseModel):
    """Result of report generation."""
    success: bool = Field(description="Whether the report generation was successful")
    report: ReportSchema = Field(description="Generated report with complete structure")
    recommendations: List[str] = Field(default_factory=list, description="Actionable recommendations")

