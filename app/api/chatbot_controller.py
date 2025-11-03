import logging

try:
    from fastapi import APIRouter, HTTPException
except Exception:
    # stubs para entorno de chequeo
    class APIRouter:
        def __init__(self):
            pass
    class HTTPException(Exception):
        def __init__(self, status_code=500, detail=None):
            super().__init__(detail)

from .schemas.chat_dto import ChatRequest
from ..service.chatbot_service import run_chatbot, clear_chat_session

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat/message")
async def chat_with_bot(body: ChatRequest):
    if not body.session_id or not body.session_id.strip():
        raise HTTPException(status_code=400, detail="session_id is required and cannot be empty")
    if not body.message or not body.message.strip():
        raise HTTPException(status_code=400, detail="message is required and cannot be empty")

    try:
        response = run_chatbot(body.session_id, body.message)
        return {"reply": response}
    except Exception:
        logger.exception("Unexpected error occurred while processing chatbot request.", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )

@router.delete("/chat/session/{session_id}")
async def delete_session(session_id: str):
    success = clear_chat_session(session_id)
    if success:
        return {"message": f"Session '{session_id}' cleared successfully"}
    return {"message": f"Session '{session_id}' not found"}
