from typing import Dict, Any
import logging
from openai import OpenAI

from ..config import OPENAI_KEY
from .schema.chat_state import ChatState
from .utils import get_or_create_history
from .tool.planificacion_analysis_tool import analyze_planificacion
from .tool.pedagogical_help_tool import get_pedagogical_help

logger = logging.getLogger(__name__)

class ReactAgentWrapper:
    def __init__(self):
        self.system_prompt = None
        self.client = None
        self._initialize()

    def _initialize(self):
        if not OPENAI_KEY:
            raise RuntimeError("OPENAI_KEY no está configurada. Por favor configure la variable de entorno en el archivo .env")

        self.client = OpenAI(api_key=OPENAI_KEY)

        # Prompt del sistema en español, conciso y enfocado en planificación docente
        self.system_prompt = (
            "Eres un asistente pedagógico llamado UTEC-Planificador. Responde en español y de forma concisa.\n"
            "Tu objetivo principal es: 1) sugerir mejoras pedagógicas para planificaciones docentes, 2) detectar inconsistencias pedagógicas básicas, 3) responder consultas de los docentes sobre el uso del planificador.\n\n"
            "IMPORTANTE - CONTEXTO DE LA PLANIFICACIÓN:\n"
            "- Si el docente tiene cargada una planificación, DEBES responder consultas relacionadas con el TEMA/MATERIA de esa planificación.\n"
            "- Ejemplo: Si la planificación es de 'Cocina 1', 'Gastronomía', etc., PUEDES Y DEBES responder sobre recetas, técnicas culinarias, etc.\n"
            "- Ejemplo: Si la planificación es de 'Química', PUEDES responder sobre elementos químicos, reacciones, etc.\n"
            "- Ejemplo: Si la planificación es de 'Educación Física', PUEDES responder sobre deportes, ejercicios, etc.\n"
            "- Tu rol es AYUDAR al docente con el CONTENIDO que necesita para su clase, no solo con la estructura de la planificación.\n\n"
            "Si el usuario solicita analizar una planificación, devuelve observaciones claras y accionables.\n"
            "Cuando utilices herramientas locales, integra sus resultados en una respuesta humana y coherente.\n\n"
            "IMPORTANTE: Conoces a fondo los ODS (Objetivos de Desarrollo Sostenible / SDGs):\n"
            "- SDG_4: Educación de calidad - Garantizar una educación inclusiva, equitativa y de calidad\n"
            "- SDG_8: Trabajo decente y crecimiento económico - Promover el empleo pleno y productivo\n"
            "- SDG_9: Industria, innovación e infraestructura - Fomentar la innovación\n"
            "- SDG_1: Fin de la pobreza | SDG_2: Hambre cero | SDG_3: Salud y bienestar\n"
            "- SDG_5: Igualdad de género | SDG_6: Agua limpia y saneamiento | SDG_7: Energía asequible\n"
            "- SDG_10: Reducción de desigualdades | SDG_11: Ciudades sostenibles | SDG_12: Producción responsable\n"
            "- SDG_13: Acción por el clima | SDG_14: Vida submarina | SDG_15: Vida terrestre\n"
            "- SDG_16: Paz y justicia | SDG_17: Alianzas para los objetivos\n"
            "Cuando un docente mencione un ODS, entiende su significado completo y cómo puede integrarse en la planificación."
        )

    def _call_openai(self, messages: list, model: str = "gpt-4o-mini") -> str:
        try:
            resp = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            if resp and resp.choices and len(resp.choices) > 0:
                return resp.choices[0].message.content.strip()
            return ""
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            raise

    def _validate_educational_relevance(self, user_input: str, planning_context: dict = None) -> tuple[bool, str]:
        """
        Valida si el prompt del usuario es relevante al contexto educativo/pedagógico.
        Retorna (is_valid, reason)
        """
        # Construir contexto adicional si hay planificación
        context_info = ""
        if planning_context:
            # Extraer información clave de la planificación en todos los niveles
            curricular_unit_name = ""
            description = planning_context.get("description", "")

            # Buscar el nombre de la unidad curricular en diferentes estructuras posibles
            if "curricularUnit" in planning_context:
                curricular_unit = planning_context["curricularUnit"]
                if isinstance(curricular_unit, dict):
                    curricular_unit_name = curricular_unit.get("name", "")
            elif "name" in planning_context:
                curricular_unit_name = planning_context.get("name", "")
            elif "subject" in planning_context:
                curricular_unit_name = planning_context.get("subject", "")

            # Extraer contenidos programáticos si existen
            programmatic_content = ""
            if "weeklyPlannings" in planning_context:
                weekly = planning_context["weeklyPlannings"]
                if isinstance(weekly, list) and len(weekly) > 0:
                    first_week = weekly[0]
                    if "programmaticContents" in first_week:
                        contents = first_week["programmaticContents"]
                        if isinstance(contents, list) and len(contents) > 0:
                            programmatic_content = contents[0].get("content", "")[:200]

            # Construir el contexto informativo
            context_info = f"\nContexto de planificación disponible:\n"
            if curricular_unit_name:
                context_info += f"- Unidad Curricular: {curricular_unit_name}\n"
            if description:
                context_info += f"- Descripción del curso: {description[:200]}\n"
            if programmatic_content:
                context_info += f"- Contenido programático: {programmatic_content}\n"

        validation_prompt = f"""
            Eres un filtro de seguridad para un asistente pedagógico educativo.

            Tu tarea es determinar si la siguiente consulta del usuario es RELEVANTE para un asistente pedagógico que ayuda a docentes con:
            - Planificaciones docentes
            - Diseño curricular
            - Estrategias de enseñanza
            - Evaluación educativa
            - Metodologías pedagógicas
            - Objetivos de aprendizaje
            - Recursos didácticos
            {context_info}
            
            Consulta del usuario: "{user_input}"
            
            REGLAS IMPORTANTES:
            1. Si hay contexto de planificación (Unidad Curricular) Y la consulta está relacionada con ESE tema específico: ES VÁLIDA
               Ejemplo: Unidad "Cocina 1" + consulta "receta de milanesa" = VÁLIDA
               Ejemplo: Unidad "Química" + consulta "tabla periódica" = VÁLIDA
               
            2. Consultas sobre CÓMO ENSEÑAR cualquier tema: SIEMPRE VÁLIDAS
               Ejemplo: "cómo enseñar cocina", "estrategias para enseñar deportes" = VÁLIDAS
               
            3. Consultas META sobre la conversación misma: SIEMPRE VÁLIDAS
               Ejemplo: "cuál fue mi último mensaje", "qué me dijiste antes", "repite eso", "explícame mejor" = VÁLIDAS
               Ejemplo: "hola", "gracias", "ok", "entiendo" = VÁLIDAS (saludos y cortesía)
               
            4. Consultas de clarificación o seguimiento: SIEMPRE VÁLIDAS
               Ejemplo: "puedes explicar mejor", "dame más detalles", "qué significa eso" = VÁLIDAS
               
            5. Consultas generales de pedagogía, didáctica, evaluación: SIEMPRE VÁLIDAS
            
            6. Consultas sobre contenido específico SIN contexto pedagógico y SIN planificación relacionada: INVÁLIDAS
               Ejemplo: Sin planificación + "receta de milanesa" = INVÁLIDA
               Ejemplo: Planificación de "Matemáticas" + "receta de pizza" = INVÁLIDA
            
            
            ANALIZA CUIDADOSAMENTE el nombre de la Unidad Curricular para determinar si la consulta es relevante.
            
            Responde SOLO con este formato:
            VÁLIDO: [SÍ o NO]
            RAZÓN: [breve explicación en una línea]
        """

        try:
            resp = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": validation_prompt}],
                temperature=0.3,
                max_tokens=150
            )

            response = resp.choices[0].message.content.strip()
            logger.info(f"Validación de relevancia: {response}")

            # Parsear la respuesta
            lines = response.split('\n')
            is_valid = False
            reason = "No se pudo determinar la relevancia"

            for line in lines:
                if line.startswith("VÁLIDO:"):
                    is_valid = "SÍ" in line.upper() or "SI" in line.upper()
                elif line.startswith("RAZÓN:"):
                    reason = line.replace("RAZÓN:", "").strip()

            return is_valid, reason

        except Exception as e:
            logger.error(f"Error en validación de relevancia: {e}")
            # En caso de error, permitir por seguridad (fail-open con warning)
            return True, "Error en validación, permitiendo por defecto"

    def invoke(self, state: ChatState) -> Dict[str, Any]:
        if not isinstance(state, ChatState):
            return {"reply": "Error: Invalid state"}

        user_text = state.input or ""

        # Validar relevancia educativa del prompt ANTES de procesar
        is_valid, reason = self._validate_educational_relevance(user_text, state.planning)

        if not is_valid:
            logger.warning(f"Prompt rechazado por no ser relevante: '{user_text}' - Razón: {reason}")
            rejection_message = (
                "Lo siento, pero solo puedo ayudarte con temas relacionados a pedagogía, "
                "enseñanza, planificación docente y educación. "
                f"\n\n¿En qué puedo asistirte con tu planificación o práctica docente?"
            )
            return {
                "reply": rejection_message,
                "session_id": state.session_id,
                "input": state.input,
                "history": []
            }

        logger.info(f"Prompt aceptado: '{user_text}' - Razón: {reason}")

        history = get_or_create_history(state.session_id)
        existing_messages = history.get_messages()

        messages = []
        # system
        messages.append({"role": "system", "content": self.system_prompt})

        # history (if any)
        for msg in existing_messages:
            # msg is expected to be dict-like with 'role' and 'content' or simple strings
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                messages.append({"role": msg['role'], "content": msg['content']})
            else:
                # fallback: treat as user message
                messages.append({"role": "user", "content": str(msg)})


        # Check if planning context is available
        planning_context = ""
        if state.planning:
            import json

            # Extraer el nombre de la unidad curricular para enfatizarlo
            curricular_unit_name = ""
            if "curricularUnit" in state.planning:
                curricular_unit = state.planning["curricularUnit"]
                if isinstance(curricular_unit, dict):
                    curricular_unit_name = curricular_unit.get("name", "")
            elif "name" in state.planning:
                curricular_unit_name = state.planning.get("name", "")

            planning_json = json.dumps(state.planning, indent=2, ensure_ascii=False)

            # Construir contexto enfatizando la unidad curricular
            planning_context = f"\n\n=== CONTEXTO DE PLANIFICACIÓN PROPORCIONADA ===\n"
            if curricular_unit_name:
                planning_context += f"**UNIDAD CURRICULAR: {curricular_unit_name}**\n"
                planning_context += f"IMPORTANTE: Debes responder consultas relacionadas con '{curricular_unit_name}'.\n\n"
            planning_context += f"Detalles completos de la planificación:\n{planning_json}\n"
            planning_context += "=" * 50 + "\n"

        # Simple tool routing based on keywords
        lower = user_text.lower()
        tool_response = None
        if any(k in lower for k in ["analiz", "analizar", "analisis", "revisión", "revisión"]):
            # call planner analysis tool — pass the user text, and planning if available
            analysis_input = user_text
            if state.planning:
                analysis_input = f"{user_text}\n\nPlanificación disponible: {planning_context}"
            tool_response = analyze_planificacion(analysis_input)
        elif any(k in lower for k in ["suger", "sugerencia", "pedagog", "retroaliment", "feedback", "rúbrica", "rubrica"]):
            help_input = user_text
            if state.planning:
                help_input = f"{user_text}\n\nPlanificación disponible: {planning_context}"
            tool_response = get_pedagogical_help(help_input)

        if tool_response:
            # integrate tool output and call LLM to format final response
            full_context = f"Herramienta: {tool_response}{planning_context}\n\nUsuario: {user_text}"
            messages.append({"role": "user", "content": full_context})
        else:
            # If no tool but planning is available, add it as context
            full_input = user_text
            if planning_context:
                full_input = f"{user_text}{planning_context}"
            messages.append({"role": "user", "content": full_input})

        try:
            reply = self._call_openai(messages)
        except Exception as e:
            logger.exception("Error calling OpenAI", exc_info=True)
            return {"reply": f"Ocurrió un error al procesar la solicitud: {e}", "session_id": state.session_id}

        # save messages into history: store as dicts
        history.add_messages([
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": reply}
        ])

        return {
            "reply": reply,
            "session_id": state.session_id,
            "input": state.input,
            "history": history.get_messages()
        }
