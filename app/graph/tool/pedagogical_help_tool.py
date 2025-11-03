def get_pedagogical_help(query: str) -> str:
    """Devuelve sugerencias pedagógicas simples basadas en la consulta del usuario.

    query: texto del usuario
    """
    # Reglas muy simples: si la consulta menciona evaluación, feedback, rúbricas, sugerir buenas prácticas.
    q = (query or "").lower()

    suggestions = []
    if "evalu" in q or "rúbrica" in q or "rubrica" in q or "calif" in q:
        suggestions.append("Considere definir rúbricas claras por actividad, vinculadas a los resultados de aprendizaje y compartirlas con los estudiantes antes de la evaluación.")
    if "feedback" in q or "retroaliment" in q:
        suggestions.append("Incluya retroalimentación formativa regular; use retroalimentación específica y accionable y combine comentarios escritos con ejemplos.")
    if "activid" in q or "actividad" in q:
        suggestions.append("Diseñe actividades activas que promuevan procesos cognitivos superiores (análisis, evaluación, creación) y aporte criterios de evaluación claros.")
    if "recurs" in q or "bibli" in q:
        suggestions.append("Asegúrese de listar recursos por semana y vincular cada recurso a una actividad y objetivo de aprendizaje.")

    if not suggestions:
        suggestions.append("¿Podría darme más contexto sobre qué aspecto pedagógico desea mejorar? Por ejemplo: evaluación, actividades, recursos, modalidades o duración de clases.")

    return "\n".join(suggestions)
