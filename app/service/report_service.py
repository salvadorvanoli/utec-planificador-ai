from typing import Dict, Any
import json
from openai import OpenAI
import os
from datetime import datetime
from app.utils.enum_descriptions import get_sdg_description

# Initialize OpenAI client
openai_client = None
OPENAI_KEY = os.getenv("OPENAI_KEY") or os.getenv("OPENAI_API_KEY")

if OPENAI_KEY:
    openai_client = OpenAI(api_key=OPENAI_KEY)


def generate_basic_report(course_id: str, statistics: Dict[str, Any], planning: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a complete report with analysis and recommendations based on course statistics and planning using GPT.

    Args:
        course_id: Course identifier
        statistics: Dictionary with complete course statistics
        planning: Dictionary with complete course planning

    Returns:
        dict with report, recommendations and overall rating
    """
    if not openai_client:
        return {
            "success": False,
            "report": {"error": "OpenAI API Key not configured"},
            "recommendations": ["Please configure OPENAI_KEY in the .env file"]
        }

    # Prepare data for GPT
    statistics_json = json.dumps(statistics, indent=2, ensure_ascii=False)
    planning_json = json.dumps(planning, indent=2, ensure_ascii=False)

    # Add SDG descriptions if present
    sdg_context = ""
    if 'linkedSDGs' in statistics and statistics['linkedSDGs']:
        sdg_descriptions = []
        for sdg_code, count in statistics['linkedSDGs'].items():
            desc = get_sdg_description(sdg_code)
            sdg_descriptions.append(f"  - {sdg_code}: {desc} (Mentioned {count} times)")
        sdg_context = "\n\nSDG CONTEXT (Objetivos de Desarrollo Sostenible):\n" + "\n".join(sdg_descriptions)

    # Prompt for GPT
    prompt = f"""
        You are an expert in pedagogical evaluation and university educational quality analysis.
    
        Analyze the following course statistics AND planning to generate a complete evaluation report:
        
        COURSE ID: {course_id}
        
        COURSE STATISTICS:
        {statistics_json}
        
        COMPLETE COURSE PLANNING:
        {planning_json}
        {sdg_context}
        
        EVALUATION CRITERIA:
        1. **Cognitive Processes**: Balance between basic levels (REMEMBER, UNDERSTAND) and higher levels (ANALYZE, EVALUATE, CREATE)
           - Optimal: 30-40% in higher levels
           - Problem: >60% in basic levels
        
        2. **Transversal Competencies**: Diversity and balance
           - Optimal: 3+ different competencies, evenly distributed
           - Problem: <3 competencies or imbalance >3:1
        
        3. **Learning Modalities**: Balance between IN_PERSON, VIRTUAL, SIMULTANEOUS_IN_PERSON_VIRTUAL, AUTONOMOUS
           - Optimal: Mix according to course nature
           - Problem: >80% in one modality without justification
        
        4. **Teaching Strategies**: Methodological variety
           - Optimal: 3+ strategies, LECTURE <50%
           - Problem: <3 strategies or LECTURE >50%
        
        5. **Activity Duration**: Appropriate time
           - Optimal: 30-90 minutes average
           - Problem: <30 or >120 minutes
        
        6. **Learning Resources**: Diversity of materials
           - Optimal: 3+ different types
           - Problem: <3 types
        
        7. **SDG Linkage (Objetivos de Desarrollo Sostenible)**: Commitment to sustainable development
           - The SDG codes (SDG_1 to SDG_17) represent specific UN development goals
           - Review the SDG CONTEXT section above for full descriptions of each goal
           - Optimal: At least 1 linked SDG with clear alignment to course objectives
           - Problem: No linkage or superficial connection without real integration
        
        8. **Delivery Format Hours**: Balance between IN_PERSON, VIRTUAL and HYBRID
           - Optimal: Balanced mix according to course nature
           - Problem: >90% in one format without justification
        
        RESPONSE FORMAT:
        Return your analysis in JSON format with this exact structure:
        {{
          "message": "Personalized message of 1-2 lines about the general state",
          "strengths": ["List of 3-5 specific positive aspects found"],
          "improvementAreas": ["List of 2-4 areas that need strengthening"],
          "recommendations": ["List of 4-8 specific and actionable recommendations with emojis"],
          "detailedAnalysis": {{
            "cognitiveProcesses": "Qualitative analysis of distribution and balance",
            "transversalCompetencies": "Analysis of diversity and balance",
            "modalityBalance": "Evaluation of modality balance",
            "teachingStrategies": "Analysis of methodological variety",
            "resources": "Evaluation of material diversity",
            "sdgLinkage": "Analysis of commitment to sustainable development"
          }}
        }}
        
        INSTRUCTIONS:
        - Use concrete data from statistics
        - Be specific with percentages and numbers
        - Recommendations should be actionable
        - Use emojis for better readability
        - Grade with rigorous but constructive pedagogical criteria
        - ALWAYS respond in Spanish
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un evaluador pedagógico experto en calidad educativa universitaria. Analizas cursos con criterio profesional basado en estándares internacionales de educación superior. Respondes siempre en español."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=2500,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        # Build final report
        report = {
            "courseId": course_id,
            "analysisDate": datetime.now().strftime("%Y-%m-%d"),
            "message": result.get("message", "Analysis completed"),
            "executiveSummary": {
                "totalWeeks": statistics.get('totalWeeks', 0),
                "totalHours": statistics.get('totalInPersonHours', 0) + statistics.get('totalVirtualHours', 0) + statistics.get('totalHybridHours', 0),
                "inPersonHours": statistics.get('totalInPersonHours', 0),
                "virtualHours": statistics.get('totalVirtualHours', 0),
                "hybridHours": statistics.get('totalHybridHours', 0),
                "averageActivityDuration": f"{statistics.get('averageActivityDurationInMinutes', 0)} min",
                "totalActivitiesAnalyzed": sum(statistics.get('cognitiveProcesses', {}).values())
            },
            "detailedAnalysis": result.get("detailedAnalysis", {}),
            "strengths": result.get("strengths", []),
            "improvementAreas": result.get("improvementAreas", [])
        }

        return {
            "success": True,
            "report": report,
            "recommendations": result.get("recommendations", [])
        }

    except Exception as e:
        # Fallback in case of error
        return {
            "success": False,
            "report": {
                "courseId": course_id,
                "error": f"Error generating report with GPT: {str(e)}"
            },
            "recommendations": ["Please try again or check your OpenAI configuration."]
        }

