"""Database repository for chat operations."""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging

from app.database.models import ChatMessage, SessionMetadata
from app.core.security import validate_all_inputs, SecurityViolation, log_security_event

logger = logging.getLogger(__name__)


class ChatRepository:
    """Repository for chat message operations."""

    def __init__(self, db: Session):
        self.db = db

    def add_message(self, session_id: str, role: str, content: str) -> ChatMessage:
        """Add a new message to the database with security validation."""
        try:
            # Validate and sanitize all inputs
            clean_session_id, clean_role, clean_content = validate_all_inputs(
                session_id, role, content
            )

            message = ChatMessage(
                session_id=clean_session_id,
                role=clean_role,
                content=clean_content
            )
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)

            self._update_session_metadata(clean_session_id)

            return message

        except SecurityViolation as e:
            log_security_event("SQL_INJECTION_ATTEMPT", {
                "session_id": session_id[:50],  # Truncate for logging
                "role": role,
                "content_length": len(content) if content else 0,
                "error": str(e)
            })
            raise

    def get_session_messages(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """Get all messages for a session, ordered by creation time (oldest to newest)."""
        from app.core.security import sanitize_session_id

        clean_session_id = sanitize_session_id(session_id)

        if limit:
            messages = self.db.query(ChatMessage).filter(
                ChatMessage.session_id == clean_session_id
            ).order_by(desc(ChatMessage.created_at)).limit(limit).all()

            messages.reverse()
            return messages

        return self.db.query(ChatMessage).filter(
            ChatMessage.session_id == clean_session_id
        ).order_by(ChatMessage.created_at).all()

    def delete_session(self, session_id: str) -> bool:
        """Delete all messages and metadata for a session."""
        from app.core.security import sanitize_session_id

        clean_session_id = sanitize_session_id(session_id)

        deleted_messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == clean_session_id
        ).delete()

        deleted_metadata = self.db.query(SessionMetadata).filter(
            SessionMetadata.session_id == clean_session_id
        ).delete()

        self.db.commit()

        return (deleted_messages + deleted_metadata) > 0

    def get_session_metadata(self, session_id: str) -> Optional[SessionMetadata]:
        """Get metadata for a session."""
        from app.core.security import sanitize_session_id

        clean_session_id = sanitize_session_id(session_id)

        return self.db.query(SessionMetadata).filter(
            SessionMetadata.session_id == clean_session_id
        ).first()

    def _update_session_metadata(self, session_id: str):
        """Update or create session metadata."""
        metadata = self.get_session_metadata(session_id)

        if metadata is None:
            metadata = SessionMetadata(
                session_id=session_id,
                message_count=1
            )
            self.db.add(metadata)
        else:
            metadata.last_activity = datetime.utcnow()
            metadata.message_count += 1

        self.db.commit()

    def get_recent_messages_count(self, session_id: str) -> int:
        """Get the count of messages in a session."""
        from app.core.security import sanitize_session_id

        clean_session_id = sanitize_session_id(session_id)

        return self.db.query(ChatMessage).filter(
            ChatMessage.session_id == clean_session_id
        ).count()

    def trim_session_messages(self, session_id: str, keep_last: int):
        """Keep only the last N messages for a session, delete older ones."""
        from app.core.security import sanitize_session_id

        clean_session_id = sanitize_session_id(session_id)

        if keep_last < 0 or keep_last > 10000:
            raise ValueError("keep_last must be between 0 and 10000")

        messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == clean_session_id
        ).order_by(desc(ChatMessage.created_at)).offset(keep_last).all()

        for message in messages:
            self.db.delete(message)

        self.db.commit()

