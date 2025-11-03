def analyze_planificacion(query: str) -> str:
    """Analiza una consulta sobre planificación docente y devuelve observaciones pedagógicas.

    query: texto con la planificación o la consulta del usuario.
    """
    text = (query or "").lower()
    observations = []

    # Detección simple de inconsistencias: falta de objetivos, duración, o recursos
    if "objet" not in text and "objetivo" not in text:
        observations.append("No se detectaron objetivos explícitos. Recomendado: describir objetivos de aprendizaje por unidad o semana.")
    if "dur" not in text and "min" not in text and "hora" not in text:
        observations.append("No se especificaron duraciones. Recomendado: indicar la duración en minutos de cada actividad.")
    if "recurso" not in text and "bibli" not in text and "referen" not in text:
        observations.append("No se listaron recursos ni bibliografía. Recomendado: añadir recursos vinculados a cada actividad.")
    if "evalu" in text and "rúbrica" not in text and "rubrica" not in text:
        observations.append("Se mencionan evaluaciones pero no rúbricas. Recomendado: incluir rúbricas y criterios claros.")

    if not observations:
        return "No se detectaron problemas evidentes en el texto provisto. Se sugiere complementar con objetivos, recursos y duración si corresponde."

    return "\n".join(observations)
