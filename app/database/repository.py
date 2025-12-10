"""Database repository for chat operations."""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging

from app.database.models import ChatMessage, SessionMetadata
from app.core.config import get_settings
from app.core.security import validate_all_inputs, SecurityViolation, log_security_event

logger = logging.getLogger(__name__)


class ChatRepository:
    """Repository for chat message operations."""

    def __init__(self, db: Session):
        self.db = db

    def add_message(self, session_id: str, role: str, content: str) -> ChatMessage:
        """
        Add a new message to the database with security validation.

        Args:
            session_id: Session identifier
            role: Message role (user, assistant, system)
            content: Message content

        Returns:
            Created ChatMessage instance

        Raises:
            SecurityViolation: If any input fails security validation
        """
        try:
            # Validate and sanitize all inputs
            clean_session_id, clean_role, clean_content = validate_all_inputs(
                session_id, role, content
            )

            # Use parameterized query through SQLAlchemy ORM
            # (ORM automatically uses parameterized queries, preventing SQL injection)
            message = ChatMessage(
                session_id=clean_session_id,
                role=clean_role,
                content=clean_content
            )
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)

            # Update session metadata
            self._update_session_metadata(clean_session_id)

            return message

        except SecurityViolation as e:
            # Log security event
            log_security_event("SQL_INJECTION_ATTEMPT", {
                "session_id": session_id[:50],  # Truncate for logging
                "role": role,
                "content_length": len(content) if content else 0,
                "error": str(e)
            })
            # Re-raise to be handled by caller
            raise

    def get_session_messages(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Get all messages for a session, ordered by creation time.

        Args:
            session_id: Session identifier
            limit: Optional limit on number of messages

        Returns:
            List of ChatMessage instances

        Raises:
            SecurityViolation: If session_id fails security validation
        """
        from app.core.security import sanitize_session_id

        # Validate session_id
        clean_session_id = sanitize_session_id(session_id)

        # Use parameterized query through SQLAlchemy ORM
        query = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == clean_session_id
        ).order_by(ChatMessage.created_at)

        if limit:
            # Get the latest N messages
            query = query.order_by(desc(ChatMessage.created_at)).limit(limit)
            messages = query.all()
            messages.reverse()  # Restore chronological order
            return messages

        return query.all()

    def delete_session(self, session_id: str) -> bool:
        """
        Delete all messages and metadata for a session.

        Args:
            session_id: Session identifier

        Returns:
            True if any records were deleted

        Raises:
            SecurityViolation: If session_id fails security validation
        """
        from app.core.security import sanitize_session_id

        # Validate session_id
        clean_session_id = sanitize_session_id(session_id)

        # Delete messages (using parameterized query through ORM)
        deleted_messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == clean_session_id
        ).delete()

        # Delete metadata (using parameterized query through ORM)
        deleted_metadata = self.db.query(SessionMetadata).filter(
            SessionMetadata.session_id == clean_session_id
        ).delete()

        self.db.commit()

        return (deleted_messages + deleted_metadata) > 0

    def get_session_metadata(self, session_id: str) -> Optional[SessionMetadata]:
        """
        Get metadata for a session.

        Args:
            session_id: Session identifier

        Returns:
            SessionMetadata instance or None

        Raises:
            SecurityViolation: If session_id fails security validation
        """
        from app.core.security import sanitize_session_id

        # Validate session_id
        clean_session_id = sanitize_session_id(session_id)

        return self.db.query(SessionMetadata).filter(
            SessionMetadata.session_id == clean_session_id
        ).first()

    def _update_session_metadata(self, session_id: str):
        """
        Update or create session metadata.

        Args:
            session_id: Session identifier (already validated by caller)
        """
        # session_id already validated by add_message, no need to revalidate
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
        """
        Get the count of messages in a session.

        Args:
            session_id: Session identifier

        Returns:
            Count of messages

        Raises:
            SecurityViolation: If session_id fails security validation
        """
        from app.core.security import sanitize_session_id

        # Validate session_id
        clean_session_id = sanitize_session_id(session_id)

        return self.db.query(ChatMessage).filter(
            ChatMessage.session_id == clean_session_id
        ).count()

    def trim_session_messages(self, session_id: str, keep_last: int):
        """
        Keep only the last N messages for a session, delete older ones.

        Args:
            session_id: Session identifier
            keep_last: Number of recent messages to keep

        Raises:
            SecurityViolation: If session_id fails security validation
        """
        from app.core.security import sanitize_session_id

        # Validate session_id
        clean_session_id = sanitize_session_id(session_id)

        # Validate keep_last is a reasonable number
        if keep_last < 0 or keep_last > 10000:
            raise ValueError("keep_last must be between 0 and 10000")

        messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == clean_session_id
        ).order_by(desc(ChatMessage.created_at)).offset(keep_last).all()

        for message in messages:
            self.db.delete(message)

        self.db.commit()

