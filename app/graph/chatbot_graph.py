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
            "Tu objetivo principal es: 1) sugerir mejoras pedagógicas para planificaciones docentes, 2) detectar inconsistencias pedagógicas básicas, 3) responder consultas de los docentes sobre el uso del planificador.\n"
            "Si el usuario solicita analizar una planificación, devuelve observaciones claras y accionables.\n"
            "Cuando utilices herramientas locales, integra sus resultados en una respuesta humana y coherente."
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

    def invoke(self, state: ChatState) -> Dict[str, Any]:
        if not isinstance(state, ChatState):
            return {"reply": "Error: Invalid state"}

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

        user_text = state.input or ""

        # Simple tool routing based on keywords
        lower = user_text.lower()
        tool_response = None
        if any(k in lower for k in ["analiz", "analizar", "analisis", "revisión", "revisión"]):
            # call planner analysis tool — pass only the user text or planning text
            tool_response = analyze_planificacion(user_text)
        elif any(k in lower for k in ["suger", "sugerencia", "pedagog", "retroaliment", "feedback", "rúbrica", "rubrica"]):
            tool_response = get_pedagogical_help(user_text)

        if tool_response:
            # integrate tool output and call LLM to format final response
            messages.append({"role": "user", "content": f"Herramienta: {tool_response}\n\nUsuario: {user_text}"})
        else:
            messages.append({"role": "user", "content": user_text})

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
