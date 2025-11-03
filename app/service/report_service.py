from typing import Dict, Any, List
import json
from openai import OpenAI
import os

# Inicializar cliente OpenAI
openai_client = None
OPENAI_KEY = os.getenv("OPENAI_KEY") or os.getenv("OPENAI_API_KEY")

if OPENAI_KEY:
    openai_client = OpenAI(api_key=OPENAI_KEY)


def generate_basic_report(course_id: str, estadisticas: Dict[str, Any]) -> Dict[str, Any]:
    """Genera un reporte completo con análisis y recomendaciones basado en estadísticas del curso usando GPT.
    
    Args:
        course_id: Identificador del curso
        estadisticas: Diccionario con estadísticas completas del curso
    
    Returns:
        dict con reporte, recomendaciones y calificación general
    """
    if not openai_client:
        return {
            "success": False,
            "reporte": {"error": "OpenAI API Key no configurada"},
            "recomendaciones": ["Por favor configure OPENAI_KEY en el archivo .env"],
            "calificacion_general": "ERROR"
        }
    
    # Preparar datos para GPT
    estadisticas_json = json.dumps(estadisticas, indent=2, ensure_ascii=False)
    
    # Prompt para GPT
    prompt = f"""
        Eres un experto en evaluación pedagógica y análisis de calidad educativa universitaria.
    
        Analiza las siguientes estadísticas de un curso y genera un reporte completo de evaluación:
        
        CURSO ID: {course_id}
        
        ESTADÍSTICAS DEL CURSO:
        {estadisticas_json}
        
        CRITERIOS DE EVALUACIÓN:
        1. **Procesos Cognitivos**: Balance entre niveles básicos (recordar, comprender) y superiores (analizar, evaluar, crear)
           - Óptimo: 30-40% en niveles superiores
           - Problema: >60% en niveles básicos
        
        2. **Competencias Transversales**: Diversidad y balance
           - Óptimo: 3+ competencias diferentes, distribuidas equitativamente
           - Problema: <3 competencias o desequilibrio >3:1
        
        3. **Modalidades**: Balance presencial/virtual
           - Óptimo: 30-70% en cada modalidad
           - Problema: >80% en una sola modalidad
        
        4. **Estrategias de Enseñanza**: Variedad metodológica
           - Óptimo: 3+ estrategias, clase expositiva <50%
           - Problema: <3 estrategias o clase expositiva >50%
        
        5. **Duración de Actividades**: Tiempo apropiado
           - Óptimo: 30-90 minutos promedio
           - Problema: <30 o >120 minutos
        
        6. **Recursos**: Diversidad de materiales
           - Óptimo: 3+ tipos diferentes
           - Problema: <3 tipos
        
        7. **Vinculación ODS**: Compromiso social
           - Óptimo: Al menos 1 ODS vinculado
           - Problema: Sin vinculación
        
        8. **Evaluación**: Enfoque formativo
           - Óptimo: Metodologías activas predominan
           - Problema: Métodos tradicionales predominan
        
        FORMATO DE RESPUESTA:
        Devuelve tu análisis en formato JSON con esta estructura exacta:
        {{
          "calificacion_general": "Una de: EXCELENTE ⭐⭐⭐⭐⭐ | MUY BUENO ⭐⭐⭐⭐ | BUENO ⭐⭐⭐ | REGULAR ⭐⭐ | NECESITA MEJORA ⭐",
          "puntuacion_numerica": 75,
          "mensaje": "Mensaje personalizado de 1-2 líneas sobre el estado general",
          "puntos_fuertes": ["Lista de 3-5 aspectos positivos específicos encontrados"],
          "areas_de_mejora": ["Lista de 2-4 áreas que necesitan fortalecimiento"],
          "recomendaciones": ["Lista de 4-8 recomendaciones específicas y accionables con emojis"],
          "analisis_detallado": {{
            "procesos_cognitivos": "Análisis cualitativo de la distribución y balance",
            "competencias_transversales": "Análisis de diversidad y equilibrio",
            "balance_modalidad": "Evaluación del balance presencial/virtual",
            "estrategias_ensenanza": "Análisis de variedad metodológica",
            "recursos": "Evaluación de diversidad de materiales",
            "vinculacion_ods": "Análisis de compromiso con desarrollo sostenible"
          }}
        }}
        
        INSTRUCCIONES:
        - Usa datos concretos de las estadísticas
        - Sé específico con porcentajes y números
        - Las recomendaciones deben ser accionables
        - Usa emojis para mejor legibilidad
        - La puntuación numérica debe estar entre 0-100
        - Califica con criterio pedagógico riguroso pero constructivo
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
        
        # Construir reporte final
        reporte = {
            "course_id": course_id,
            "fecha_analisis": "2025-01-17",
            "calificacion_general": result.get("calificacion_general", "BUENO ⭐⭐⭐"),
            "puntuacion": f"{result.get('puntuacion_numerica', 70)}%",
            "mensaje": result.get("mensaje", "Análisis completado"),
            "resumen_ejecutivo": {
                "total_semanas": estadisticas.get('totalSemanas', 0),
                "total_horas": estadisticas.get('totalHorasPresenciales', 0) + estadisticas.get('totalHorasVirtuales', 0),
                "horas_presenciales": estadisticas.get('totalHorasPresenciales', 0),
                "horas_virtuales": estadisticas.get('totalHorasVirtuales', 0),
                "duracion_promedio_actividades": f"{estadisticas.get('promedioDuracionActividadesMin', 0)} min",
                "total_actividades_analizadas": sum(estadisticas.get('procesosCognitivos', {}).values())
            },
            "analisis_detallado": result.get("analisis_detallado", {}),
            "puntos_fuertes": result.get("puntos_fuertes", []),
            "areas_de_mejora": result.get("areas_de_mejora", [])
        }
        
        return {
            "success": True,
            "reporte": reporte,
            "recomendaciones": result.get("recomendaciones", []),
            "calificacion_general": result.get("calificacion_general", "BUENO ⭐⭐⭐")
        }
        
    except Exception as e:
        # Fallback en caso de error
        return {
            "success": False,
            "reporte": {
                "course_id": course_id,
                "error": f"Error al generar reporte con GPT: {str(e)}"
            },
            "recomendaciones": ["Por favor intente nuevamente o verifique su configuración de OpenAI."],
            "calificacion_general": "ERROR"
        }
