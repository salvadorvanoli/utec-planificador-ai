from typing import Dict, Any
import json
from openai import OpenAI
import os
from app.utils.enum_descriptions import get_sdgs_with_descriptions

# Initialize OpenAI client
openai_client = None
OPENAI_KEY = os.getenv("OPENAI_KEY") or os.getenv("OPENAI_API_KEY")

if OPENAI_KEY:
    openai_client = OpenAI(api_key=OPENAI_KEY)


def _normalize_to_string(value: Any) -> str:
    """Convert LLM output to a readable string.

    - If list, joins into numbered lines.
    - If dict, converts to JSON with indentation.
    - If None or empty, returns empty string.
    - Otherwise, returns str(value).
    """
    if value is None:
        return ""
    if isinstance(value, list):
        lines = []
        for i, item in enumerate(value, start=1):
            if isinstance(item, (dict, list)):
                item_str = json.dumps(item, ensure_ascii=False)
            else:
                item_str = str(item)
            lines.append(f"{i}. {item_str}")
        return "\n".join(lines)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def generate_suggestions(planning_data: Dict[str, Any], context: dict = None) -> dict:
    """Generate pedagogical suggestions based on complete course planning using GPT.

    Args:
        planning_data: Dictionary with all course planning information
        context: Additional context (course_id, etc.)

    Returns:
        dict with 'analysis' and 'pedagogicalSuggestions'
    """
    if not openai_client:
        return {
            "analysis": "Error: OpenAI API Key not configured",
            "pedagogicalSuggestions": "Please configure OPENAI_KEY in the .env file"
        }

    context = context or {}

    # Extract key information from planning
    description = planning_data.get('description', '')
    weekly_plannings = planning_data.get('weeklyPlannings', [])
    sdgs = planning_data.get('sustainableDevelopmentGoals', [])
    udl_principles = planning_data.get('universalDesignLearningPrinciples', [])
    hours_per_format = planning_data.get('hoursPerDeliveryFormat', {})
    in_person_hours = hours_per_format.get('IN_PERSON', 0)
    virtual_hours = hours_per_format.get('VIRTUAL', 0)
    hybrid_hours = hours_per_format.get('HYBRID', 0)
    grading_system = planning_data.get('partialGradingSystem', '')
    curricular_unit = planning_data.get('curricularUnit', {})
    shift = planning_data.get('shift', '')

    # Analyze cognitive processes, strategies, and competencies
    cognitive_processes = []
    strategies = []
    competencies = []
    resources = []
    modalities = []

    for week in weekly_plannings:
        # Direct week activities
        for activity in week.get('activities', []):
            cognitive_processes.extend(activity.get('cognitiveProcesses', []))
            strategies.extend(activity.get('teachingStrategies', []))
            competencies.extend(activity.get('transversalCompetencies', []))
            resources.extend(activity.get('learningResources', []))
            modality = activity.get('learningModality')
            if modality:
                modalities.append(modality)

        # Activities within programmatic contents
        for content in week.get('programmaticContents', []):
            for activity in content.get('activities', []):
                cognitive_processes.extend(activity.get('cognitiveProcesses', []))
                strategies.extend(activity.get('teachingStrategies', []))
                competencies.extend(activity.get('transversalCompetencies', []))
                resources.extend(activity.get('learningResources', []))
                modality = activity.get('learningModality')
                if modality:
                    modalities.append(modality)

    # Prepare summary for GPT
    total_activities = sum(
        len(w.get('activities', [])) +
        sum(len(c.get('activities', [])) for c in w.get('programmaticContents', []))
        for w in weekly_plannings
    )

    # Format SDGs with their full descriptions
    sdgs_formatted = get_sdgs_with_descriptions(sdgs) if sdgs else "Ningún ODS vinculado"

    summary = {
        "description": description,
        "curricularUnit": curricular_unit.get('name', 'N/A'),
        "credits": curricular_unit.get('credits', 0),
        "shift": shift,
        "totalWeeks": len(weekly_plannings),
        "totalActivities": total_activities,
        "inPersonHours": in_person_hours,
        "virtualHours": virtual_hours,
        "hybridHours": hybrid_hours,
        "linkedSDGs": sdgs_formatted,
        "udlPrinciples": udl_principles,
        "gradingSystem": grading_system,
        "cognitiveProcessesUsed": list(set(cognitive_processes)),
        "strategiesUsed": list(set(s for s in strategies if s)),
        "competenciesWorked": list(set(competencies)),
        "resourcesUtilized": list(set(resources)),
        "modalitiesUsed": list(set(modalities)),
        "linkedToResearch": planning_data.get('isRelatedToInvestigation', False),
        "linkedToProductiveSector": planning_data.get('involvesActivitiesWithProductiveSector', False)
    }

    # Prompt for GPT
    prompt = f"""
        You are an expert in pedagogical design and university teaching planning.

        Analyze the following course planning and provide:
        1. A detailed analysis of the pedagogical structure
        2. Concrete improvement suggestions based on educational best practices
        
        PLANNING TO ANALYZE:
        {json.dumps(summary, indent=2, ensure_ascii=False)}
        
        ANALYSIS CONTEXT:
        - Evaluate the balance between in-person, virtual, and hybrid hours
        - Analyze the diversity of cognitive processes according to Bloom's Revised Taxonomy
        - Verify the application of UDL (Universal Design for Learning) principles
        - **Review linkage with SDGs (Sustainable Development Goals / Objetivos de Desarrollo Sostenible)**: 
          The linkedSDGs field contains the FULL DESCRIPTIONS of each SDG, not just codes.
          Analyze how the course content and activities align with these specific development goals.
          Provide concrete suggestions on how to strengthen this connection.
        - Evaluate the variety of teaching strategies
        - Analyze the development of transversal competencies
        - Review the partial grading system (should be formative and continuous)
        - Evaluate linkage with research and productive sector
        - Analyze the diversity of learning resources used
        - Consider the learning modalities used (VIRTUAL, IN_PERSON, SIMULTANEOUS_IN_PERSON_VIRTUAL, AUTONOMOUS)
        
        RESPONSE FORMAT:
        Return your analysis in JSON format with this exact structure:
        {{
          "analysis": "Detailed analysis of the planning with metrics and specific observations. Use emojis for better readability. Response in Spanish.",
          "pedagogicalSuggestions": "Numbered list of 5-8 concrete and actionable suggestions to improve the planning. If the planning is excellent, congratulate and give 2-3 advanced-level recommendations. Response in Spanish."
        }}
        
        IMPORTANT: 
        - Be specific and constructive
        - Use appropriate pedagogical terminology
        - Suggestions should be actionable
        - If something is good, acknowledge it before suggesting improvements
        - ALWAYS respond in Spanish
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un pedagogo experto especializado en diseño curricular universitario y mejores prácticas educativas. Respondes siempre en español de forma clara y profesional."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
            response_format={
                "type": "json_object"
            }
        )

        # Try to convert response to JSON; if it fails, use the full string
        raw_content = response.choices[0].message.content
        try:
            result = json.loads(raw_content)
        except Exception:
            result = {"analysis": raw_content, "pedagogicalSuggestions": ""}

        analysis = result.get("analysis", "Could not generate analysis")
        pedagogical = result.get("pedagogicalSuggestions", "Could not generate suggestions")

        pedagogical_str = _normalize_to_string(pedagogical)

        return {
            "analysis": analysis,
            "pedagogicalSuggestions": pedagogical_str
        }

    except Exception as e:
        # Fallback in case of error
        return {
            "analysis": f"Error generating analysis with GPT: {str(e)}",
            "pedagogicalSuggestions": "Please try again or check your OpenAI configuration."
        }

