"""Chatbot API endpoints."""
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api.v2.dtos import ChatRequest, ChatHistoryResponse
from app.services.chatbot_service import ChatbotService
from app.database.models import get_db
from app.core.security import SecurityViolation

router = APIRouter(tags=["Chatbot"])
logger = logging.getLogger(__name__)

chatbot_service = ChatbotService()


@router.post("/chat/message")
async def chat_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Process a chat message and return the assistant's response.
    """
    if not request.session_id or not request.session_id.strip():
        raise HTTPException(
            status_code=400,
            detail="session_id is required and cannot be empty"
        )

    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="message is required and cannot be empty"
        )

    try:
        planning_dict = None
        if request.coursePlanning:
            planning_dict = request.coursePlanning.model_dump()

        response = chatbot_service.process_message(
            db=db,
            session_id=request.session_id,
            user_message=request.message,
            planning=planning_dict
        )

        return {"reply": response}

    except SecurityViolation as e:
        logger.error(f"Security violation in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Your input contains suspicious patterns or invalid characters. Please try again with different text."
        )

    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )


@router.delete("/chat/session/{session_id}")
async def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a chat session and all its messages.
    """
    try:
        success = chatbot_service.clear_session(db, session_id)

        if success:
            return {"message": f"Session '{session_id}' cleared successfully"}
        else:
            return {"message": f"Session '{session_id}' not found"}

    except SecurityViolation as e:
        logger.error(f"Security violation in delete_session: {e}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID format"
        )

    except Exception as e:
        logger.error(f"Error deleting session: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error deleting session"
        )


@router.get("/chat/session/{session_id}/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get conversation history for a session.
    """
    try:
        messages = chatbot_service.get_session_history(db, session_id)
        return ChatHistoryResponse(messages=messages)

    except SecurityViolation as e:
        logger.error(f"Security violation in get_chat_history: {e}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID format"
        )

    except Exception as e:
        logger.error(f"Error retrieving history: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error retrieving chat history"
        )

