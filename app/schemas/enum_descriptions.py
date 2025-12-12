"""Enum descriptions and mappings for the UTEC Planning System.

This module provides human-readable descriptions for all enums used in the system.
These descriptions are used by:
- AI agents to understand context better
- Report generation to provide detailed explanations
- Services to format user-friendly messages
"""
from typing import Dict, List


# ==================== SUSTAINABLE DEVELOPMENT GOALS (ODS) ====================

SDG_DESCRIPTIONS = {
    "SDG_1": "Fin de la pobreza - Poner fin a la pobreza en todas sus formas en todo el mundo",
    "SDG_2": "Hambre cero - Poner fin al hambre, lograr la seguridad alimentaria y la mejora de la nutrición",
    "SDG_3": "Salud y bienestar - Garantizar una vida sana y promover el bienestar para todos en todas las edades",
    "SDG_4": "Educación de calidad - Garantizar una educación inclusiva, equitativa y de calidad y promover oportunidades de aprendizaje durante toda la vida para todos",
    "SDG_5": "Igualdad de género - Lograr la igualdad entre los géneros y empoderar a todas las mujeres y las niñas",
    "SDG_6": "Agua limpia y saneamiento - Garantizar la disponibilidad de agua y su gestión sostenible y el saneamiento para todos",
    "SDG_7": "Energía asequible y no contaminante - Garantizar el acceso a una energía asequible, segura, sostenible y moderna para todos",
    "SDG_8": "Trabajo decente y crecimiento económico - Promover el crecimiento económico sostenido, inclusivo y sostenible, el empleo pleno y productivo y el trabajo decente para todos",
    "SDG_9": "Industria, innovación e infraestructura - Construir infraestructuras resilientes, promover la industrialización inclusiva y sostenible y fomentar la innovación",
    "SDG_10": "Reducción de las desigualdades - Reducir la desigualdad en y entre los países",
    "SDG_11": "Ciudades y comunidades sostenibles - Lograr que las ciudades y los asentamientos humanos sean inclusivos, seguros, resilientes y sostenibles",
    "SDG_12": "Producción y consumo responsables - Garantizar modalidades de consumo y producción sostenibles",
    "SDG_13": "Acción por el clima - Adoptar medidas urgentes para combatir el cambio climático y sus efectos",
    "SDG_14": "Vida submarina - Conservar y utilizar en forma sostenible los océanos, los mares y los recursos marinos para el desarrollo sostenible",
    "SDG_15": "Vida de ecosistemas terrestres - Proteger, restablecer y promover el uso sostenible de los ecosistemas terrestres, gestionar los bosques de forma sostenible, luchar contra la desertificación",
    "SDG_16": "Paz, justicia e instituciones sólidas - Promover sociedades pacíficas e inclusivas para el desarrollo sostenible, facilitar el acceso a la justicia para todos",
    "SDG_17": "Alianzas para lograr los objetivos - Fortalecer los medios de ejecución y revitalizar la Alianza Mundial para el Desarrollo Sostenible"
}


# ==================== COGNITIVE PROCESSES (BLOOM'S TAXONOMY) ====================

COGNITIVE_PROCESS_DESCRIPTIONS = {
    "REMEMBER": "Recordar - Recuperar, reconocer y recordar conocimiento relevante de la memoria a largo plazo",
    "UNDERSTAND": "Comprender - Construir significado a partir de material educativo, incluyendo la comunicación oral, escrita y gráfica",
    "APPLY": "Aplicar - Usar información y conocimiento en una nueva situación o contexto",
    "ANALYZE": "Analizar - Descomponer información en partes, determinar cómo se relacionan entre sí y con la estructura general",
    "EVALUATE": "Evaluar - Hacer juicios basados en criterios y estándares mediante comprobación y crítica",
    "CREATE": "Crear - Juntar elementos para formar algo nuevo y coherente, o reorganizar elementos en un nuevo patrón o estructura",
    "NOT_DETERMINED": "Sin determinar - No se ha especificado el proceso cognitivo"
}


# ==================== TRANSVERSAL COMPETENCIES ====================

TRANSVERSAL_COMPETENCY_DESCRIPTIONS = {
    "COMMUNICATION": "Comunicación - Capacidad de expresar ideas de forma clara, coherente y efectiva tanto oralmente como por escrito",
    "TEAMWORK": "Trabajo en equipo - Capacidad de colaborar con otros de manera efectiva hacia un objetivo común, respetando roles y perspectivas",
    "LEARNING_SELF_REGULATION": "Autorregulación del aprendizaje - Capacidad de planificar, monitorear, evaluar y ajustar el propio proceso de aprendizaje",
    "CRITICAL_THINKING": "Pensamiento crítico - Capacidad de analizar, evaluar, sintetizar información y formar juicios fundamentados",
    "NOT_DETERMINED": "Sin determinar - No se ha especificado la competencia transversal"
}


# ==================== LEARNING MODALITIES ====================

LEARNING_MODALITY_DESCRIPTIONS = {
    "VIRTUAL": "Virtual - Aprendizaje a distancia mediante plataformas digitales, sin presencia física en el aula",
    "IN_PERSON": "Presencial - Aprendizaje en el aula física con interacción directa entre docentes y estudiantes",
    "SIMULTANEOUS_IN_PERSON_VIRTUAL": "Simultáneamente presencial-virtual - Modalidad híbrida sincrónica donde algunos estudiantes están presentes y otros conectados virtualmente",
    "AUTONOMOUS": "Autónomo - Aprendizaje autodirigido por el estudiante, sin sincronía con el docente",
    "NOT_DETERMINED": "Sin determinar - No se ha especificado la modalidad de aprendizaje"
}


# ==================== TEACHING STRATEGIES ====================

TEACHING_STRATEGY_DESCRIPTIONS = {
    "LECTURE": "Clase magistral - Exposición estructurada del docente sobre un tema específico",
    "DEBATE": "Debate - Discusión estructurada donde se presentan y defienden diferentes posiciones sobre un tema",
    "TEAMWORK": "Trabajo en equipo - Actividades colaborativas grupales donde los estudiantes trabajan juntos",
    "FIELD_ACTIVITY": "Actividad de campo - Trabajo práctico fuera del aula en contextos reales (empresas, comunidades, etc.)",
    "PRACTICAL_ACTIVITY": "Actividad práctica - Ejercicios aplicados donde se pone en práctica lo aprendido",
    "LABORATORY_PRACTICES": "Prácticas de laboratorio - Experimentos y prácticas técnicas en laboratorios especializados",
    "TESTS": "Pruebas - Evaluaciones formativas o sumativas para medir el aprendizaje",
    "RESEARCH_ACTIVITIES": "Actividades de investigación - Proyectos de indagación científica o académica",
    "FLIPPED_CLASSROOM": "Aula invertida - Metodología donde el estudio teórico se hace en casa y la práctica en clase",
    "DISCUSSION": "Discusión - Intercambio de ideas guiado por el docente sobre temas específicos",
    "SMALL_GROUP_TUTORIALS": "Tutorías en grupos pequeños - Atención personalizada a grupos reducidos de estudiantes",
    "PROJECTS": "Proyectos - Trabajo extendido aplicado que integra múltiples competencias y conocimientos",
    "CASE_STUDY": "Caso de estudio - Análisis profundo de situaciones reales para extraer aprendizajes",
    "OTHER": "Otros - Estrategias alternativas no categorizadas",
    "NOT_DETERMINED": "Sin determinar - No se ha especificado la estrategia de enseñanza"
}


# ==================== LEARNING RESOURCES ====================

LEARNING_RESOURCE_DESCRIPTIONS = {
    "EXHIBITION": "Exhibición - Presentaciones visuales, demostrativas o expositivas",
    "BOOK_DOCUMENT": "Libro/documento - Material de lectura impreso o digital (libros, artículos, papers)",
    "DEMONSTRATION": "Demostración - Muestra práctica de procedimientos, técnicas o procesos",
    "WHITEBOARD": "Pizarrón - Pizarra tradicional o digital para explicaciones visuales",
    "ONLINE_COLLABORATION_TOOL": "Herramienta de colaboración en línea - Plataformas colaborativas (Google Docs, Miro, Padlet, etc.)",
    "ONLINE_LECTURE": "Charla en línea - Videoconferencias o webinars sincrónicos",
    "ONLINE_FORUM": "Foro en línea - Espacios de discusión asíncrona para intercambio de ideas",
    "ONLINE_EVALUATION": "Evaluación en línea - Pruebas, cuestionarios y exámenes digitales",
    "GAME": "Juego - Gamificación, juegos serios y actividades lúdicas educativas",
    "SURVEY": "Encuesta - Instrumentos de retroalimentación y recolección de opiniones",
    "VIDEO": "Video - Material audiovisual educativo (grabaciones, tutoriales, documentales)",
    "INFOGRAPHIC": "Infografía - Representaciones visuales sintéticas de información compleja",
    "WEBPAGE": "Página web - Recursos en línea, sitios web educativos y contenido digital",
    "OTHER": "Otros - Recursos alternativos no categorizados",
    "NOT_DETERMINED": "Sin determinar - No se ha especificado el recurso de aprendizaje"
}


# ==================== UNIVERSAL DESIGN FOR LEARNING (UDL) PRINCIPLES ====================

UDL_PRINCIPLE_DESCRIPTIONS = {
    "MEANS_OF_ENGAGEMENT": "Medios de compromiso (UDL) - Proporcionar múltiples formas de motivar e involucrar a los estudiantes en el aprendizaje",
    "MEANS_OF_REPRESENTATION": "Medios de representación (UDL) - Proporcionar múltiples formas de presentar información y contenido a los estudiantes",
    "MEANS_OF_ACTION_EXPRESSION": "Medios de acción y expresión (UDL) - Proporcionar múltiples formas para que los estudiantes demuestren lo que han aprendido",
    "NONE": "Ninguno - No se aplican principios UDL en esta actividad"
}


# ==================== DELIVERY FORMAT ====================

DELIVERY_FORMAT_DESCRIPTIONS = {
    "IN_PERSON": "Presencial - Clases realizadas completamente en el campus universitario",
    "VIRTUAL": "Virtual - Clases completamente en línea a través de plataformas digitales",
    "HYBRID": "Híbrido - Combinación de clases presenciales y virtuales"
}


# ==================== SHIFT ====================

SHIFT_DESCRIPTIONS = {
    "MORNING": "Matutino - Turno mañana (generalmente 8:00 - 13:00)",
    "EVENING": "Vespertino - Turno tarde/noche (generalmente 18:00 - 22:00)"
}


# ==================== PARTIAL GRADING SYSTEM (SCP - Sistemas de Calificación de Parciales) ====================
# Basado en la Circular de Evaluaciones, Calificaciones e Inasistencias de UTEC

PARTIAL_GRADING_SYSTEM_DESCRIPTIONS = {
    "SCP_1": "SCP 1 - Primera evaluación: 25%, Segunda evaluación: 35%, Evaluación Continua: 40%",
    "SCP_2": "SCP 2 - Primera evaluación: 30%, Segunda evaluación: 30%, Evaluación Continua: 40%",
    "SCP_3": "SCP 3 - Primera evaluación: 25%, Segunda evaluación: 35%, Laboratorio: 20%, Evaluación Continua: 20%",
    "SCP_4": "SCP 4 - Participación en trabajo: 70%, Trabajo entregado: 30%",
    "SCP_5": "SCP 5 - Primera evaluación: 30%, Segunda evaluación: 50%, Tercera evaluación: 20% (para trabajos finales)",
    "SCP_6": "SCP 6 - Actividades: 60%, Participación: 40% (para carreras virtuales)",
    "SCP_7": "SCP 7 - Primera evaluación: 50%, Segunda evaluación: 50% (para tecnólogos compartidos UTU-UTEC-Udelar)",
    "SCP_8": "SCP 8 - Primera evaluación: 40%, Segunda evaluación: 60% (para tecnólogos compartidos UTU-UTEC-Udelar)",
    "SCP_9": "SCP 9 - Actividades Teórico-Prácticas: 70%, Evaluación Continua: 30%",
    "SCP_10": "SCP 10 - Participación en el trabajo: 70%, Trabajo entregado: 30% (para inglés)",
    "SCP_11": "SCP 11 - Laboratorio: 30%, Evaluación Continua: 10%, Proyecto: 20%, Primera-Cuarta Evaluación: 10% c/u (sin examen)",
    "SCP_12": "SCP 12 - Laboratorios: 30%, Evaluación Continua: 30%, Proyecto: 40% (sin examen, para talleres)"
}


# ==================== DOMAIN AREAS ====================

DOMAIN_AREA_DESCRIPTIONS = {
    "INSTALLATION_DESIGN": "Diseño de instalaciones - Planificación y diseño técnico de sistemas e infraestructuras",
    "INSTALLATION_MANAGEMENT": "Gestión de instalaciones - Administración y mantenimiento de instalaciones existentes",
    "RDI_PROJECTS": "Proyectos de I+D+i - Investigación, Desarrollo e Innovación tecnológica",
    "SERVICE_MANAGEMENT": "Gestión de servicios - Administración de servicios técnicos y profesionales"
}


# ==================== PROFESSIONAL COMPETENCIES ====================

PROFESSIONAL_COMPETENCY_DESCRIPTIONS = {
    "TECHNICAL_ASSISTANCE": "Asistencia técnica - Brindar soporte técnico especializado",
    "EFFICIENT_MANAGEMENT": "Gestión eficiente - Administrar recursos de manera óptima",
    "MAINTENANCE_PLANNING": "Planificación de mantenimiento - Programar y organizar tareas de mantenimiento",
    "INSTITUTIONAL_ADVISORY": "Asesoramiento institucional - Consultoría a organizaciones",
    "PERSONNEL_TRAINING": "Capacitación de personal - Formación y desarrollo de equipos",
    "COMPLIANCE_VERIFICATION": "Verificación de cumplimiento - Auditoría de normas y estándares",
    "PROJECT_DESIGN_MANAGEMENT": "Diseño y gestión de proyectos - Planificación y dirección de proyectos técnicos",
    "DIRECTOR_ACTIVITIES": "Actividades de dirección - Liderazgo y toma de decisiones estratégicas",
    "ESTABLISHMENT_MANAGEMENT": "Gestión de establecimientos - Administración integral de instalaciones"
}


# ==================== HELPER FUNCTIONS ====================

def get_sdg_description(sdg_code: str) -> str:
    """Get the full description of an SDG by its code.

    Args:
        sdg_code: SDG code (e.g., "SDG_1", "SDG_17")

    Returns:
        Human-readable description of the SDG
    """
    return SDG_DESCRIPTIONS.get(sdg_code, f"Descripción no disponible para {sdg_code}")


def get_sdgs_with_descriptions(sdg_list: List[str]) -> str:
    """Convert a list of SDG codes to a formatted string with descriptions.

    Args:
        sdg_list: List of SDG codes

    Returns:
        Formatted multi-line string with SDGs and descriptions
    """
    if not sdg_list:
        return "Ningún ODS vinculado"

    result = []
    for sdg in sdg_list:
        desc = SDG_DESCRIPTIONS.get(sdg, sdg)
        result.append(f"- {desc}")

    return "\n".join(result)


def get_cognitive_processes_with_descriptions(processes: List[str]) -> str:
    """Convert a list of cognitive processes to a formatted string with descriptions.

    Args:
        processes: List of cognitive process codes

    Returns:
        Formatted multi-line string with processes and descriptions
    """
    if not processes:
        return "No especificado"

    result = []
    for process in set(processes):  # Use set to avoid duplicates
        desc = COGNITIVE_PROCESS_DESCRIPTIONS.get(process, process)
        result.append(f"- {desc}")

    return "\n".join(result)


def get_enum_description(enum_type: str, enum_value: str) -> str:
    """Get description for any enum type and value.

    Args:
        enum_type: Type of enum (e.g., "SDG", "COGNITIVE_PROCESS", "TEACHING_STRATEGY")
        enum_value: Value of the enum (e.g., "SDG_1", "REMEMBER", "LECTURE")

    Returns:
        Human-readable description
    """
    mappings = {
        "SDG": SDG_DESCRIPTIONS,
        "COGNITIVE_PROCESS": COGNITIVE_PROCESS_DESCRIPTIONS,
        "TRANSVERSAL_COMPETENCY": TRANSVERSAL_COMPETENCY_DESCRIPTIONS,
        "LEARNING_MODALITY": LEARNING_MODALITY_DESCRIPTIONS,
        "TEACHING_STRATEGY": TEACHING_STRATEGY_DESCRIPTIONS,
        "LEARNING_RESOURCE": LEARNING_RESOURCE_DESCRIPTIONS,
        "UDL_PRINCIPLE": UDL_PRINCIPLE_DESCRIPTIONS,
        "DELIVERY_FORMAT": DELIVERY_FORMAT_DESCRIPTIONS,
        "SHIFT": SHIFT_DESCRIPTIONS,
        "PARTIAL_GRADING_SYSTEM": PARTIAL_GRADING_SYSTEM_DESCRIPTIONS,
        "DOMAIN_AREA": DOMAIN_AREA_DESCRIPTIONS,
        "PROFESSIONAL_COMPETENCY": PROFESSIONAL_COMPETENCY_DESCRIPTIONS
    }

    mapping = mappings.get(enum_type, {})
    return mapping.get(enum_value, enum_value)


def get_all_descriptions_for_prompt() -> str:
    """Get all enum descriptions formatted for AI prompts.

    Returns:
        Formatted string with all descriptions for context injection in prompts
    """
    sections = [
        ("OBJETIVOS DE DESARROLLO SOSTENIBLE (ODS)", SDG_DESCRIPTIONS),
        ("PROCESOS COGNITIVOS (Taxonomía de Bloom)", COGNITIVE_PROCESS_DESCRIPTIONS),
        ("COMPETENCIAS TRANSVERSALES", TRANSVERSAL_COMPETENCY_DESCRIPTIONS),
        ("MODALIDADES DE APRENDIZAJE", LEARNING_MODALITY_DESCRIPTIONS),
        ("ESTRATEGIAS DE ENSEÑANZA", TEACHING_STRATEGY_DESCRIPTIONS),
        ("RECURSOS DE APRENDIZAJE", LEARNING_RESOURCE_DESCRIPTIONS),
        ("PRINCIPIOS DE DISEÑO UNIVERSAL PARA EL APRENDIZAJE (UDL)", UDL_PRINCIPLE_DESCRIPTIONS),
    ]

    result = []
    for title, descriptions in sections:
        result.append(f"\n### {title}")
        for key, value in descriptions.items():
            result.append(f"- {key}: {value}")

    return "\n".join(result)

