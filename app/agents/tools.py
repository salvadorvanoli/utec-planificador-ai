"""Tools for the pedagogical agent."""
from typing import Optional


def analyze_planning_structure(planning_text: str) -> str:
    """
    Analyze the structure of a planning document.

    Args:
        planning_text: The text to analyze

    Returns:
        Analysis observations
    """
    text_lower = planning_text.lower()
    observations = []

    # Check for explicit objectives
    if "objet" not in text_lower and "objetivo" not in text_lower:
        observations.append(
            "No se detectaron objetivos explícitos. "
            "Recomendación: Describir objetivos de aprendizaje por unidad o semana."
        )

    # Check for duration specifications
    if all(term not in text_lower for term in ["dur", "min", "hora"]):
        observations.append(
            "No se especificaron duraciones. "
            "Recomendación: Indicar la duración en minutos de cada actividad."
        )

    # Check for resources
    if all(term not in text_lower for term in ["recurso", "bibli", "referen"]):
        observations.append(
            "No se listaron recursos ni bibliografía. "
            "Recomendación: Añadir recursos vinculados a cada actividad."
        )

    # Check for evaluation rubrics
    if "evalu" in text_lower and "rúbrica" not in text_lower and "rubrica" not in text_lower:
        observations.append(
            "Se mencionan evaluaciones pero no rúbricas. "
            "Recomendación: Incluir rúbricas y criterios claros."
        )

    if not observations:
        return (
            "No se detectaron problemas evidentes en el texto provisto. "
            "Se sugiere complementar con objetivos, recursos y duración si corresponde."
        )

    return "\n".join(observations)


def get_pedagogical_tips(query: str) -> str:
    """
    Provide pedagogical tips based on the user query.

    Args:
        query: The user's question

    Returns:
        Pedagogical suggestions
    """
    query_lower = query.lower()
    suggestions = []

    # Evaluation and rubrics
    if any(term in query_lower for term in ["evalu", "rúbrica", "rubrica", "calif"]):
        suggestions.append(
            "Considere definir rúbricas claras por actividad, vinculadas a los resultados "
            "de aprendizaje y compartirlas con los estudiantes antes de la evaluación."
        )

    # Feedback
    if any(term in query_lower for term in ["feedback", "retroaliment"]):
        suggestions.append(
            "Incluya retroalimentación formativa regular; use retroalimentación específica "
            "y accionable y combine comentarios escritos con ejemplos."
        )

    # Activities
    if "activid" in query_lower:
        suggestions.append(
            "Diseñe actividades activas que promuevan procesos cognitivos superiores "
            "(análisis, evaluación, creación) y aporte criterios de evaluación claros."
        )

    # Resources
    if any(term in query_lower for term in ["recurs", "bibli"]):
        suggestions.append(
            "Asegúrese de listar recursos por semana y vincular cada recurso a una "
            "actividad y objetivo de aprendizaje."
        )

    if not suggestions:
        suggestions.append(
            "¿Podría darme más contexto sobre qué aspecto pedagógico desea mejorar? "
            "Por ejemplo: evaluación, actividades, recursos, modalidades o duración de clases."
        )

    return "\n".join(suggestions)

