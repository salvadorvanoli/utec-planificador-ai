"""LangGraph-based pedagogical chatbot agent."""
import json
import logging
from typing import Dict, Any, List
from openai import OpenAI
from langgraph.graph import StateGraph, END

from app.agents.state import ChatState
from app.core.config import get_settings
from app.core.prompts import (
    SYSTEM_PROMPT,
    VALIDATION_PROMPT_TEMPLATE
)
from app.core.json_schemas import VALIDATION_JSON_SCHEMA

logger = logging.getLogger(__name__)


class PedagogicalAgent:
    """LangGraph-based agent for pedagogical assistance."""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(ChatState)
        
        # Add nodes
        workflow.add_node("validate_input", self._validate_input)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("handle_invalid", self._handle_invalid_input)
        
        # Set entry point
        workflow.set_entry_point("validate_input")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "validate_input",
            self._should_generate_response,
            {
                "generate": "generate_response",
                "reject": "handle_invalid"
            }
        )
        
        # Add edges to end
        workflow.add_edge("generate_response", END)
        workflow.add_edge("handle_invalid", END)
        
        return workflow.compile()
    
    def _validate_input(self, state: ChatState) -> ChatState:
        """Validate if the user input is educationally relevant."""
        user_input = state["user_input"]
        planning = state.get("planning")

        # Build planning context if available
        context_info = self._build_planning_context(planning)
        
        # Use LLM for validation
        validation_prompt = VALIDATION_PROMPT_TEMPLATE.format(
            context_info=context_info,
            user_input=user_input
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "user", "content": validation_prompt}
                ],
                temperature=0.3,
                max_tokens=150,
                response_format=VALIDATION_JSON_SCHEMA
            )
            
            response_text = response.choices[0].message.content.strip()

            # Parse JSON (guaranteed to be valid by schema)
            result = json.loads(response_text)

            state["is_valid"] = result["is_valid"]
            state["validation_reason"] = result["reason"]

            logger.info(f"Validación: {'VÁLIDA' if result['is_valid'] else 'INVÁLIDA'} - {result['reason']}")

        except Exception as e:
            logger.error(f"Validation error: {e}")
            # In case of error, be permissive
            state["is_valid"] = True
            state["validation_reason"] = "Validation error - defaulting to valid"
        
        return state
    
    def _build_planning_context(self, planning: Dict[str, Any]) -> str:
        """Build context information from planning data."""
        if not planning:
            return ""
        
        context_parts = ["\nContexto de planificación disponible:"]
        
        # Extract curricular unit name
        curricular_unit_name = ""
        if "curricularUnit" in planning:
            curricular_unit = planning["curricularUnit"]
            if isinstance(curricular_unit, dict):
                curricular_unit_name = curricular_unit.get("name", "")
        elif "name" in planning:
            curricular_unit_name = planning.get("name", "")
        elif "subject" in planning:
            curricular_unit_name = planning.get("subject", "")
        
        if curricular_unit_name:
            context_parts.append(f"- Unidad Curricular: {curricular_unit_name}")
        
        # Extract description
        description = planning.get("description", "")
        if description:
            context_parts.append(f"- Descripción del curso: {description[:200]}")
        
        # Extract programmatic content
        if "weeklyPlannings" in planning:
            weekly = planning["weeklyPlannings"]
            if isinstance(weekly, list) and weekly:
                first_week = weekly[0]
                if "programmaticContents" in first_week:
                    contents = first_week["programmaticContents"]
                    if isinstance(contents, list) and contents:
                        content_text = contents[0].get("content", "")[:200]
                        if content_text:
                            context_parts.append(f"- Contenido programático: {content_text}")
        
        return "\n".join(context_parts)
    
    def _should_generate_response(self, state: ChatState) -> str:
        """Determine next step based on validation."""
        return "generate" if state.get("is_valid", False) else "reject"
    
    def _generate_response(self, state: ChatState) -> ChatState:
        """Generate AI response using OpenAI."""
        messages = state["messages"]
        user_input = state["user_input"]
        planning = state.get("planning")

        # Build conversation messages for OpenAI
        openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add conversation history
        for msg in messages:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Add planning context if available
        # The LLM will decide how to use this information based on the user's query
        planning_context = ""
        if planning:
            # Extract curricular unit name
            curricular_unit_name = ""
            if "curricularUnit" in planning:
                curricular_unit = planning["curricularUnit"]
                if isinstance(curricular_unit, dict):
                    curricular_unit_name = curricular_unit.get("name", "")
            elif "name" in planning:
                curricular_unit_name = planning.get("name", "")

            planning_json = json.dumps(planning, indent=2, ensure_ascii=False)

            # Build context with planning information
            planning_context = f"\n\n=== CONTEXTO DE PLANIFICACIÓN DISPONIBLE ===\n"
            if curricular_unit_name:
                planning_context += f"Unidad Curricular: {curricular_unit_name}\n\n"
            planning_context += f"Planificación completa:\n{planning_json}\n"
            planning_context += "=" * 50 + "\n"
            planning_context += (
                "Nota: Usa esta información solo si es relevante para la consulta del usuario. "
                "No analices la planificación a menos que el usuario lo solicite explícitamente.\n"
            )

        # Add current user input with planning context if available
        full_input = user_input
        if planning_context:
            full_input = f"{user_input}{planning_context}"

        openai_messages.append({"role": "user", "content": full_input})

        try:
            response = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=openai_messages,
                temperature=self.settings.openai_temperature,
                max_tokens=self.settings.openai_max_tokens
            )
            
            assistant_message = response.choices[0].message.content.strip()
            state["response"] = assistant_message
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            state["response"] = (
                "Lo siento, hubo un error al procesar tu solicitud. "
                "Por favor, intenta nuevamente."
            )
        
        return state
    
    def _handle_invalid_input(self, state: ChatState) -> ChatState:
        """Handle invalid input."""
        state["response"] = (
            "Lo siento, esta consulta no parece estar relacionada con pedagogía, "
            "planificación docente o educación. Como asistente pedagógico, puedo ayudarte con:\n\n"
            "• Diseño de planificaciones y actividades educativas\n"
            "• Estrategias de enseñanza y evaluación\n"
            "• Metodologías pedagógicas (Bloom, UDL, etc.)\n"
            "• Objetivos de Desarrollo Sostenible (ODS)\n"
            "• Información sobre UTEC y sus programas\n\n"
            "¿En qué puedo ayudarte con tu planificación docente?"
        )
        return state
    
    def run(
        self,
        session_id: str,
        user_input: str,
        messages: List[Dict[str, str]],
        planning: Dict[str, Any] = None
    ) -> str:
        """
        Run the agent with user input.
        
        Args:
            session_id: Session identifier
            user_input: User's message
            messages: Conversation history
            planning: Optional planning context
            
        Returns:
            Agent's response
        """
        state: ChatState = {
            "session_id": session_id,
            "user_input": user_input,
            "planning": planning,
            "messages": messages,
            "response": None,
            "is_valid": None,
            "validation_reason": None
        }
        
        result = self.graph.invoke(state)
        return result["response"]

