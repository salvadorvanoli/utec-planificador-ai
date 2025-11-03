from typing import Dict, Any
import json
from openai import OpenAI
import os

# Inicializar cliente OpenAI
openai_client = None
OPENAI_KEY = os.getenv("OPENAI_KEY") or os.getenv("OPENAI_API_KEY")

if OPENAI_KEY:
    openai_client = OpenAI(api_key=OPENAI_KEY)


def _normalize_to_string(value: Any) -> str:
    """Convierte la salida del LLM a una cadena legible.

    - Si es lista, la une en líneas numeradas.
    - Si es dict, la convierte a JSON con indentación.
    - Si es None o vacío, devuelve cadena vacía.
    - En cualquier otro caso, devuelve str(value).
    """
    if value is None:
        return ""
    if isinstance(value, list):
        # si ya viene numerada, mantenemos; en caso contrario enumeramos
        lines = []
        for i, item in enumerate(value, start=1):
            # item puede ser dict o str
            if isinstance(item, (dict, list)):
                item_str = json.dumps(item, ensure_ascii=False)
            else:
                item_str = str(item)
            lines.append(f"{i}. {item_str}")
        return "\n".join(lines)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def generate_suggestions(planificacion_data: Dict[str, Any], context: dict = None) -> dict:
    """Genera sugerencias pedagógicas basadas en la planificación docente completa usando GPT.
    
    Args:
        planificacion_data: Diccionario con toda la información de la planificación docente
        context: Contexto adicional (course_id, etc.)
    
    Returns:
        dict con 'analysis' y 'pedagogical_suggestions'
    """
    if not openai_client:
        return {
            "analysis": "Error: OpenAI API Key no configurada",
            "pedagogical_suggestions": "Por favor configure OPENAI_KEY en el archivo .env"
        }
    
    context = context or {}
    
    # Extraer información clave de la planificación
    desc_general = planificacion_data.get('descripcionGeneral', '')
    semanas = planificacion_data.get('semanas', [])
    ods = planificacion_data.get('objetivosDesarrolloSostenibleVinculados', [])
    dua = planificacion_data.get('principiosDUA', [])
    horas_presenciales = planificacion_data.get('horasPresenciales', 0)
    horas_virtuales = planificacion_data.get('horasVirtuales', 0)
    sistema_calificacion = planificacion_data.get('sistemaDeCalificacion', '')
    
    # Analizar procesos cognitivos, estrategias y competencias
    procesos_cognitivos = []
    estrategias = []
    competencias = []
    
    for semana in semanas:
        for actividad in semana.get('actividades', []):
            procesos_cognitivos.extend(actividad.get('procesosCognitivos', []))
            if actividad.get('estrategiaEnseñanza'):
                estrategias.append(actividad.get('estrategiaEnseñanza'))
            competencias.extend(actividad.get('competenciasTransversales', []))
    
    # Preparar resumen para GPT
    resumen = {
        "descripcion": desc_general,
        "total_semanas": len(semanas),
        "total_actividades": sum(len(s.get('actividades', [])) for s in semanas),
        "horas_presenciales": horas_presenciales,
        "horas_virtuales": horas_virtuales,
        "ods_vinculados": ods,
        "principios_dua": dua,
        "sistema_calificacion": sistema_calificacion,
        "procesos_cognitivos_usados": list(set(procesos_cognitivos)),
        "estrategias_usadas": list(set(e for e in estrategias if e)),
        "competencias_trabajadas": list(set(competencias))
    }
    
    # Prompt para GPT
    prompt = f"""
        Eres un experto en diseño pedagógico y planificación docente universitaria. 

        Analiza la siguiente planificación docente y proporciona:
        1. Un análisis detallado de la estructura pedagógica
        2. Sugerencias concretas de mejora basadas en mejores prácticas educativas
        
        PLANIFICACIÓN A ANALIZAR:
        {json.dumps(resumen, indent=2, ensure_ascii=False)}
        
        CONTEXTO DE ANÁLISIS:
        - Evalúa el balance entre horas presenciales y virtuales
        - Analiza la diversidad de procesos cognitivos según la Taxonomía de Bloom revisada
        - Verifica la aplicación de principios DUA (Diseño Universal para el Aprendizaje)
        - Revisa la vinculación con ODS (Objetivos de Desarrollo Sostenible)
        - Evalúa la variedad de estrategias de enseñanza
        - Analiza el desarrollo de competencias transversales
        - Revisa el sistema de calificación (debe ser formativo y continuo)
        
        FORMATO DE RESPUESTA:
        Devuelve tu análisis en formato JSON con esta estructura exacta:
        {{
          "analysis": "Análisis detallado de la planificación con métricas y observaciones específicas. Usa emojis para mejor legibilidad.",
          "pedagogical_suggestions": "Lista numerada de 5-8 sugerencias concretas y accionables para mejorar la planificación. Si la planificación es excelente, felicita y da 2-3 recomendaciones de nivel avanzado."
        }}
        
        IMPORTANTE: 
        - Sé específico y constructivo
        - Usa terminología pedagógica apropiada
        - Las sugerencias deben ser accionables
        - Si algo está bien, reconócelo antes de sugerir mejoras
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto pedagogo especializado en diseño curricular universitario y mejores prácticas educativas. Respondes siempre en español de forma clara y profesional."
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
        
        # Intentamos convertir la respuesta a JSON; si falla, usamos la cadena completa
        raw_content = response.choices[0].message.content
        try:
            result = json.loads(raw_content)
        except Exception:
            # si el LLM devolvió texto plano, intentamos extraer un bloque JSON; si no, devolvemos el texto como análisis
            result = {"analysis": raw_content, "pedagogical_suggestions": ""}

        analysis = result.get("analysis", "No se pudo generar el análisis")
        pedagogical = result.get("pedagogical_suggestions", "No se pudieron generar sugerencias")

        pedagogical_str = _normalize_to_string(pedagogical)

        return {
            "analysis": analysis,
            "pedagogical_suggestions": pedagogical_str
        }
        
    except Exception as e:
        # Fallback en caso de error
        return {
            "analysis": f"Error al generar análisis con GPT: {str(e)}",
            "pedagogical_suggestions": "Por favor intente nuevamente o verifique su configuración de OpenAI."
        }
