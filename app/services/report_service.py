"""Report generation service."""
import json
import logging
from typing import Dict, Any
from datetime import datetime
from openai import OpenAI

from app.core.config import get_settings
from app.core.prompts import REPORT_PROMPT_TEMPLATE
from app.core.constants import get_sdg_description
from app.core.json_schemas import REPORT_JSON_SCHEMA
from app.api.schemas.report_schemas import (
    ReportGenerationResult,
    ReportSchema,
    ExecutiveSummarySchema,
    DetailedAnalysisSchema
)

logger = logging.getLogger(__name__)


class ReportService:
    """Service for generating pedagogical reports."""

    def __init__(self):
        self.settings = get_settings()

        # Validate API key
        if not self.settings.openai_api_key:
            logger.error("OPENAI_KEY is not configured in environment variables")
            raise ValueError("OpenAI API key is not configured")

        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def generate_report(
        self,
        course_id: str,
        statistics: Dict[str, Any],
        planning: Dict[str, Any]
    ) -> ReportGenerationResult:
        """
        Generate a pedagogical evaluation report.

        Args:
            course_id: Course identifier
            statistics: Course statistics
            planning: Complete course planning

        Returns:
            Dictionary with report data
        """
        try:
            # Format data for the prompt
            statistics_json = json.dumps(statistics, indent=2, ensure_ascii=False)
            planning_json = json.dumps(planning, indent=2, ensure_ascii=False)

            # Build SDG context
            sdg_context = self._build_sdg_context(statistics)

            # Generate prompt
            prompt = REPORT_PROMPT_TEMPLATE.format(
                statistics=statistics_json,
                planning=planning_json,
                sdg_context=sdg_context
            )

            # Call OpenAI with structured output (uses JSON schema constant)
            response = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en evaluación pedagógica y calidad educativa."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format=REPORT_JSON_SCHEMA
            )

            content = response.choices[0].message.content.strip()
            logger.info(f"OpenAI raw response length: {len(content)} characters")
            logger.debug(f"OpenAI response preview: {content[:200]}...")

            # Try to parse as JSON
            try:
                # Extract JSON if wrapped in markdown code blocks
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                report_data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.warning(f"Raw content: {content[:500]}")
                # Fallback: structure the response manually with complete structure
                report_data = {
                    "message": "Análisis completado",
                    "detailedAnalysis": {
                        "cognitiveProcesses": "El análisis está siendo procesado.",
                        "transversalCompetencies": "El análisis está siendo procesado.",
                        "modalityBalance": "El análisis está siendo procesado.",
                        "teachingStrategies": "El análisis está siendo procesado.",
                        "resources": "El análisis está siendo procesado.",
                        "sdgLinkage": "El análisis está siendo procesado."
                    },
                    "strengths": ["El curso presenta elementos pedagógicos positivos"],
                    "improvementAreas": ["Ver recomendaciones para áreas específicas de mejora"],
                    "recommendations": [content] if content else ["Intenta regenerar el reporte"]
                }

            # Build executive summary using schema (guarantees structure)
            executive_summary = ExecutiveSummarySchema(
                totalWeeks=statistics.get('totalWeeks', 0),
                totalHours=(
                    statistics.get('totalInPersonHours', 0) +
                    statistics.get('totalVirtualHours', 0) +
                    statistics.get('totalHybridHours', 0)
                ),
                inPersonHours=statistics.get('totalInPersonHours', 0),
                virtualHours=statistics.get('totalVirtualHours', 0),
                hybridHours=statistics.get('totalHybridHours', 0),
                averageActivityDuration=f"{statistics.get('averageActivityDurationInMinutes', 0)} min",
                totalActivitiesAnalyzed=sum(statistics.get('cognitiveProcesses', {}).values())
            )

            # Build detailed analysis using schema
            detailed_analysis_data = report_data.get("detailedAnalysis", {})
            detailed_analysis = DetailedAnalysisSchema(
                cognitiveProcesses=detailed_analysis_data.get("cognitiveProcesses", ""),
                transversalCompetencies=detailed_analysis_data.get("transversalCompetencies", ""),
                modalityBalance=detailed_analysis_data.get("modalityBalance", ""),
                teachingStrategies=detailed_analysis_data.get("teachingStrategies", ""),
                resources=detailed_analysis_data.get("resources", ""),
                sdgLinkage=detailed_analysis_data.get("sdgLinkage", "")
            )

            # Build complete report using schema
            report = ReportSchema(
                courseId=course_id,
                analysisDate=datetime.now().strftime("%Y-%m-%d"),
                message=report_data.get("message", "Analysis completed"),
                executiveSummary=executive_summary,
                detailedAnalysis=detailed_analysis,
                strengths=report_data.get("strengths", []),
                improvementAreas=report_data.get("improvementAreas", [])
            )

            # Return using result schema
            return ReportGenerationResult(
                success=True,
                report=report,
                recommendations=report_data.get("recommendations", [])
            )

        except Exception as e:
            logger.error(f"Error generating report: {e}", exc_info=True)

            # Return error response with proper schema structure
            error_report = ReportSchema(
                courseId=course_id,
                analysisDate=datetime.now().strftime("%Y-%m-%d"),
                message="Error al generar el reporte. Por favor, intenta nuevamente.",
                executiveSummary=ExecutiveSummarySchema(),  # Empty with defaults
                detailedAnalysis=DetailedAnalysisSchema(),  # Empty with defaults
                strengths=[],
                improvementAreas=[]
            )

            return ReportGenerationResult(
                success=False,
                report=error_report,
                recommendations=["Por favor, verifica los datos y intenta nuevamente."]
            )

    def _build_sdg_context(self, statistics: Dict[str, Any]) -> str:
        """Build SDG context section."""
        if "linkedSDGs" not in statistics or not statistics["linkedSDGs"]:
            return ""

        sdg_descriptions = []
        for sdg_code, count in statistics["linkedSDGs"].items():
            description = get_sdg_description(sdg_code)
            sdg_descriptions.append(f"  - {sdg_code}: {description} (Mencionado {count} veces)")

        return "\n\nCONTEXTO DE ODS (Objetivos de Desarrollo Sostenible):\n" + "\n".join(sdg_descriptions)

