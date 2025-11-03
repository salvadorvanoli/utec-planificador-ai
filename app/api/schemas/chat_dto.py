try:
    from pydantic import BaseModel
except Exception:
    class BaseModel:
        pass

class ChatRequest(BaseModel):
    session_id: str
    message: str
