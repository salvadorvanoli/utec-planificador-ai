"""
Enum descriptions and mappings for the UTEC Planning System.
This module provides human-readable descriptions for all enums used in the system.
"""

# Sustainable Development Goals (ODS) - Full descriptions
SDG_DESCRIPTIONS = {
    "SDG_1": "Poner fin a la pobreza en todas sus formas en todo el mundo.",
    "SDG_2": "Poner fin al hambre, lograr la seguridad.",
    "SDG_3": "Garantizar una vida sana y promover el bienestar para todos en todas las edades.",
    "SDG_4": "Garantizar una educación inclusiva, equitativa y de calidad y promover oportunidades de aprendizaje durante toda la vida para todos.",
    "SDG_5": "Lograr la igualdad entre los géneros y empoderar a todas las mujeres y las niñas.",
    "SDG_6": "Garantizar la disponibilidad de agua y su gestión sostenible y el saneamiento para todos.",
    "SDG_7": "Garantizar el acceso a una energía asequible, segura, sostenible y moderna para todos.",
    "SDG_8": "Promover el crecimiento económico sostenido, inclusivo y sostenible, el empleo pleno y productivo y el trabajo decente para todos.",
    "SDG_9": "Construir infraestructuras resilientes, promover la industrialización inclusiva y sostenible y fomentar la innovación.",
    "SDG_10": "Reducir la desigualdad en y entre los países.",
    "SDG_11": "Lograr que las ciudades y los asentamientos humanos sean inclusivos, seguros, resilientes y sostenibles.",
    "SDG_12": "Garantizar modalidades de consumo y producción sostenibles.",
    "SDG_13": "Adoptar medidas urgentes para combatir el cambio climático y sus efectos.",
    "SDG_14": "Conservar y utilizar en forma sostenible los océanos, los mares y los recursos marinos para el desarrollo sostenible.",
    "SDG_15": "Proteger, restablecer y promover el uso sostenible de los ecosistemas terrestres, gestionar los bosques de forma sostenible, luchar contra la desertificación, detener e invertir la degradación de las tierras y poner freno a la pérdida de la diversidad biológica.",
    "SDG_16": "Promover sociedades pacíficas e inclusivas para el desarrollo sostenible, facilitar el acceso a la justicia para todos y crear instituciones eficaces, responsables e inclusivas a todos los niveles.",
    "SDG_17": "Fortalecer los medios de ejecución y revitalizar la Alianza Mundial para el Desarrollo Sostenible."
}

# Cognitive Processes (Bloom's Taxonomy) - Spanish descriptions
COGNITIVE_PROCESS_DESCRIPTIONS = {
    "REMEMBER": "Recordar - Recuperar conocimiento de la memoria a largo plazo",
    "UNDERSTAND": "Comprender - Construir significado a partir de material educativo",
    "APPLY": "Aplicar - Usar información en una nueva situación",
    "ANALYZE": "Analizar - Descomponer información en partes y determinar relaciones",
    "EVALUATE": "Evaluar - Hacer juicios basados en criterios y estándares",
    "CREATE": "Crear - Juntar elementos para formar algo nuevo y coherente",
    "NOT_DETERMINED": "Sin determinar"
}

# Transversal Competencies - Spanish descriptions
TRANSVERSAL_COMPETENCY_DESCRIPTIONS = {
    "COMMUNICATION": "Comunicación - Capacidad de expresar ideas de forma clara y efectiva",
    "TEAMWORK": "Trabajo en equipo - Capacidad de colaborar con otros hacia un objetivo común",
    "LEARNING_SELF_REGULATION": "Autorregulación del aprendizaje - Capacidad de planificar, monitorear y evaluar el propio aprendizaje",
    "CRITICAL_THINKING": "Pensamiento crítico - Capacidad de analizar, evaluar y sintetizar información",
    "NOT_DETERMINED": "Sin determinar"
}

# Learning Modalities - Spanish descriptions
LEARNING_MODALITY_DESCRIPTIONS = {
    "VIRTUAL": "Virtual - Aprendizaje a distancia mediante plataformas digitales",
    "IN_PERSON": "Presencial - Aprendizaje en el aula física",
    "SIMULTANEOUS_IN_PERSON_VIRTUAL": "Simultáneamente presencial-virtual - Híbrido sincrónico",
    "AUTONOMOUS": "Autónomo - Aprendizaje autodirigido por el estudiante",
    "NOT_DETERMINED": "Sin determinar"
}

# Teaching Strategies - Spanish descriptions
TEACHING_STRATEGY_DESCRIPTIONS = {
    "LECTURE": "Clase magistral - Exposición del docente",
    "DEBATE": "Debate - Discusión estructurada de temas",
    "TEAMWORK": "Trabajo en equipo - Actividades colaborativas grupales",
    "FIELD_ACTIVITY": "Actividad de campo - Trabajo práctico fuera del aula",
    "PRACTICAL_ACTIVITY": "Actividad práctica - Ejercicios aplicados",
    "LABORATORY_PRACTICES": "Prácticas de laboratorio - Experimentos y prácticas técnicas",
    "TESTS": "Pruebas - Evaluaciones formativas o sumativas",
    "RESEARCH_ACTIVITIES": "Actividades de investigación - Proyectos de indagación",
    "FLIPPED_CLASSROOM": "Aula invertida - Estudio previo y práctica en clase",
    "DISCUSSION": "Discusión - Intercambio de ideas guiado",
    "SMALL_GROUP_TUTORIALS": "Tutorías en grupos pequeños - Atención personalizada",
    "PROJECTS": "Proyectos - Trabajo extendido aplicado",
    "CASE_STUDY": "Caso de estudio - Análisis de situaciones reales",
    "OTHER": "Otros - Estrategias alternativas",
    "NOT_DETERMINED": "Sin determinar"
}

# Learning Resources - Spanish descriptions
LEARNING_RESOURCE_DESCRIPTIONS = {
    "EXHIBITION": "Exhibición - Presentaciones visuales o demostrativas",
    "BOOK_DOCUMENT": "Libro/documento - Material de lectura",
    "DEMONSTRATION": "Demostración - Muestra práctica de procedimientos",
    "WHITEBOARD": "Pizarrón - Pizarra tradicional o digital",
    "ONLINE_COLLABORATION_TOOL": "Herramienta de colaboración en línea - Plataformas colaborativas",
    "ONLINE_LECTURE": "Charla en línea - Videoconferencias",
    "ONLINE_FORUM": "Foro en línea - Espacios de discusión asíncrona",
    "ONLINE_EVALUATION": "Evaluación en línea - Pruebas y cuestionarios digitales",
    "GAME": "Juego - Gamificación y juegos educativos",
    "SURVEY": "Encuesta - Instrumentos de retroalimentación",
    "VIDEO": "Video - Material audiovisual",
    "INFOGRAPHIC": "Infografía - Representaciones visuales de información",
    "WEBPAGE": "Página web - Recursos en línea",
    "OTHER": "Otros - Recursos alternativos",
    "NOT_DETERMINED": "Sin determinar"
}

# Universal Design for Learning Principles - Spanish descriptions
UDL_PRINCIPLE_DESCRIPTIONS = {
    "MEANS_OF_ENGAGEMENT": "Medios de compromiso - Múltiples formas de motivar e involucrar",
    "MEANS_OF_REPRESENTATION": "Medios de representación - Múltiples formas de presentar información",
    "MEANS_OF_ACTION_EXPRESSION": "Medios de acción y expresión - Múltiples formas de demostrar aprendizaje",
    "NONE": "Ninguno"
}

# Delivery Format - Spanish descriptions
DELIVERY_FORMAT_DESCRIPTIONS = {
    "IN_PERSON": "Presencial - Clases en el campus",
    "VIRTUAL": "Virtual - Clases completamente en línea",
    "HYBRID": "Híbrido - Combinación de presencial y virtual"
}

# Shift - Spanish descriptions
SHIFT_DESCRIPTIONS = {
    "MORNING": "Matutino - Turno mañana",
    "EVENING": "Vespertino - Turno tarde/noche"
}


def get_sdg_description(sdg_code: str) -> str:
    """Get the full description of an SDG by its code."""
    return SDG_DESCRIPTIONS.get(sdg_code, sdg_code)


def get_sdgs_with_descriptions(sdg_list: list) -> str:
    """Convert a list of SDG codes to a formatted string with descriptions."""
    if not sdg_list:
        return "Ningún ODS vinculado"

    result = []
    for sdg in sdg_list:
        desc = SDG_DESCRIPTIONS.get(sdg, sdg)
        result.append(f"- {sdg}: {desc}")

    return "\n".join(result)


def get_cognitive_processes_with_descriptions(processes: list) -> str:
    """Convert a list of cognitive processes to a formatted string with descriptions."""
    if not processes:
        return "No especificado"

    result = []
    for process in set(processes):
        desc = COGNITIVE_PROCESS_DESCRIPTIONS.get(process, process)
        result.append(f"- {desc}")

    return "\n".join(result)


def get_enum_description(enum_type: str, enum_value: str) -> str:
    """Get description for any enum type and value."""
    mappings = {
        "SDG": SDG_DESCRIPTIONS,
        "COGNITIVE_PROCESS": COGNITIVE_PROCESS_DESCRIPTIONS,
        "TRANSVERSAL_COMPETENCY": TRANSVERSAL_COMPETENCY_DESCRIPTIONS,
        "LEARNING_MODALITY": LEARNING_MODALITY_DESCRIPTIONS,
        "TEACHING_STRATEGY": TEACHING_STRATEGY_DESCRIPTIONS,
        "LEARNING_RESOURCE": LEARNING_RESOURCE_DESCRIPTIONS,
        "UDL_PRINCIPLE": UDL_PRINCIPLE_DESCRIPTIONS,
        "DELIVERY_FORMAT": DELIVERY_FORMAT_DESCRIPTIONS,
        "SHIFT": SHIFT_DESCRIPTIONS
    }

    mapping = mappings.get(enum_type, {})
    return mapping.get(enum_value, enum_value)

