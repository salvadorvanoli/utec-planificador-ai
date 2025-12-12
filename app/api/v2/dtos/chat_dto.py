from pydantic import BaseModel
from typing import Optional, List
from .planification_dto import CoursePlanningDTO


class ChatRequest(BaseModel):
    session_id: str
    message: str
    coursePlanning: Optional[CoursePlanningDTO] = None


class ChatMessageDTO(BaseModel):
    """DTO for a single chat message."""
    role: str
    content: str
    timestamp: str


class ChatHistoryResponse(BaseModel):
    """DTO for chat history response."""
    messages: List[ChatMessageDTO]


