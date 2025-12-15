"""Chatbot service layer."""
import logging
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from app.agents.chatbot_agent import PedagogicalAgent
from app.database.repository import ChatRepository
from app.core.config import get_settings
from app.core.security import SecurityViolation
from app.api.v2.dtos import ChatMessageDTO

logger = logging.getLogger(__name__)


class ChatbotService:
    """Service for chatbot operations."""

    def __init__(self):
        self.agent = PedagogicalAgent()
        self.settings = get_settings()

    def process_message(
        self,
        db: Session,
        session_id: str,
        user_message: str,
        planning: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process a user message and return the agent's response."""
        repo = ChatRepository(db)

        message_limit = self.settings.session_max_messages
        db_messages = repo.get_session_messages(session_id, limit=message_limit)

        messages = [msg.to_dict() for msg in db_messages]

        try:
            response = self.agent.run(
                session_id=session_id,
                user_input=user_message,
                messages=messages,
                planning=planning
            )
        except Exception as e:
            logger.error(f"Error running agent: {e}", exc_info=True)
            response = (
                "Lo siento, ocurrió un error inesperado. "
                "Por favor, intenta nuevamente más tarde."
            )

        try:
            repo.add_message(session_id, "user", user_message)
        except SecurityViolation as e:
            logger.error(f"Security violation when saving user message: {e}")
            return "Lo siento, tu mensaje contiene caracteres o patrones no permitidos por seguridad."

        try:
            repo.add_message(session_id, "assistant", response)
        except SecurityViolation as e:
            logger.error(f"Security violation when saving assistant message: {e}")
            return response

        total_messages = repo.get_recent_messages_count(session_id)
        if total_messages > message_limit * 2:
            repo.trim_session_messages(session_id, message_limit * 2)

        return response

    def clear_session(self, db: Session, session_id: str) -> bool:
        """Clear a chat session."""
        repo = ChatRepository(db)
        return repo.delete_session(session_id)

    def get_session_history(self, db: Session, session_id: str) -> List[ChatMessageDTO]:
        """Get conversation history for a session."""
        repo = ChatRepository(db)
        messages = repo.get_session_messages(session_id)
        return [
            ChatMessageDTO(
                role=msg.role,
                content=msg.content,
                timestamp=msg.created_at.isoformat()
            )
            for msg in messages
        ]

