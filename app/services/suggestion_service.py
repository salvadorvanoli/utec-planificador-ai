"""Suggestion generation service."""
import json
import logging
from typing import Dict, Any
from openai import OpenAI

from app.core.prompts import SUGGESTION_PROMPT_TEMPLATE
from app.core.json_schemas import SUGGESTION_JSON_SCHEMA
from app.api.schemas.suggestion_schemas import SuggestionGenerationResult
from app.core.config import get_settings

logger = logging.getLogger(__name__)


class SuggestionService:
    """Service for generating pedagogical suggestions."""

    def __init__(self):
        self.settings = get_settings()

        # Validate API key
        if not self.settings.openai_api_key:
            logger.error("OPENAI_KEY is not configured in environment variables")
            raise ValueError("OpenAI API key is not configured")

        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def generate_suggestions(
        self,
        planning_data: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> SuggestionGenerationResult:
        """
        Generate pedagogical suggestions based on course planning.

        Args:
            planning_data: Complete course planning data
            context: Additional context (course_id, etc.)

        Returns:
            SuggestionGenerationResult with analysis and suggestions
        """
        context = context or {}

        try:
            # Build planning summary
            summary = self._build_planning_summary(planning_data)

            # Generate prompt
            prompt = SUGGESTION_PROMPT_TEMPLATE.format(planning_summary=summary)

            # Call OpenAI with structured output (uses JSON schema constant)
            response = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en pedagogía universitaria y diseño curricular."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                response_format=SUGGESTION_JSON_SCHEMA
            )

            content = response.choices[0].message.content.strip()

            # Parse JSON (guaranteed to be valid by schema)
            result = json.loads(content)

            # Return using Pydantic schema
            return SuggestionGenerationResult(
                analysis=result["analysis"],
                pedagogicalSuggestions=result["pedagogicalSuggestions"]
            )

        except Exception as e:
            logger.error(f"Error generating suggestions: {e}", exc_info=True)
            return SuggestionGenerationResult(
                analysis="Error al generar el análisis. Por favor, intenta nuevamente.",
                pedagogicalSuggestions="Error al generar sugerencias. Por favor, intenta nuevamente."
            )

    def _build_planning_summary(self, planning_data: Dict[str, Any]) -> str:
        """Build a summary of the planning data for the prompt."""
        summary_parts = []

        # Basic information
        description = planning_data.get("description", "")
        if description:
            summary_parts.append(f"**Descripción del curso:**\n{description}\n")

        # Delivery format hours
        hours_per_format = planning_data.get("hoursPerDeliveryFormat", {})
        if hours_per_format:
            summary_parts.append("**Horas por formato de entrega:**")
            for format_type, hours in hours_per_format.items():
                summary_parts.append(f"- {format_type}: {hours} horas")
            summary_parts.append("")

        # SDGs
        sdgs = planning_data.get("sustainableDevelopmentGoals", [])
        if sdgs:
            summary_parts.append(f"**ODS vinculados:** {', '.join(sdgs)}\n")

        # UDL principles
        udl = planning_data.get("universalDesignLearningPrinciples", [])
        if udl:
            summary_parts.append(f"**Principios UDL:** {', '.join(udl)}\n")

        # Analyze activities
        weekly_plannings = planning_data.get("weeklyPlannings", [])
        cognitive_processes = []
        strategies = []
        competencies = []
        modalities = []

        for week in weekly_plannings:
            # Direct activities
            for activity in week.get("activities", []):
                cognitive_processes.extend(activity.get("cognitiveProcesses", []))
                strategies.extend(activity.get("teachingStrategies", []))
                competencies.extend(activity.get("transversalCompetencies", []))
                modality = activity.get("learningModality")
                if modality:
                    modalities.append(modality)

            # Activities within programmatic contents
            for content in week.get("programmaticContents", []):
                for activity in content.get("activities", []):
                    cognitive_processes.extend(activity.get("cognitiveProcesses", []))
                    strategies.extend(activity.get("teachingStrategies", []))
                    competencies.extend(activity.get("transversalCompetencies", []))
                    modality = activity.get("learningModality")
                    if modality:
                        modalities.append(modality)

        # Count and summarize
        if cognitive_processes:
            process_counts = self._count_items(cognitive_processes)
            summary_parts.append("**Procesos cognitivos:**")
            for process, count in sorted(process_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                summary_parts.append(f"- {process}: {count}")
            summary_parts.append("")

        if strategies:
            strategy_counts = self._count_items(strategies)
            summary_parts.append("**Estrategias de enseñanza:**")
            for strategy, count in sorted(strategy_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                summary_parts.append(f"- {strategy}: {count}")
            summary_parts.append("")

        if competencies:
            competency_counts = self._count_items(competencies)
            summary_parts.append("**Competencias transversales:**")
            for competency, count in sorted(competency_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                summary_parts.append(f"- {competency}: {count}")
            summary_parts.append("")

        total_activities = sum(
            len(w.get("activities", [])) + sum(len(c.get("activities", [])) for c in w.get("programmaticContents", []))
            for w in weekly_plannings
        )

        summary_parts.append(f"**Total de actividades:** {total_activities}")
        summary_parts.append(f"**Semanas planificadas:** {len(weekly_plannings)}")

        return "\n".join(summary_parts)

    def _count_items(self, items: list) -> Dict[str, int]:
        """Count occurrences of items in a list."""
        counts = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        return counts

