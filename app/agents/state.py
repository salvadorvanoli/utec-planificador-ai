"""LangGraph state definition."""
from typing import TypedDict, List, Optional, Dict, Any


class ChatState(TypedDict):
    """State for the chat graph."""
    session_id: str
    user_input: str
    planning: Optional[Dict[str, Any]]
    messages: List[Dict[str, str]]
    response: Optional[str]
    is_valid: Optional[bool]
    validation_reason: Optional[str]

