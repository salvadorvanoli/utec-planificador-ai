try:
    from pydantic import BaseModel
    from typing import Optional
except Exception:
    class BaseModel:
        pass
    Optional = None

from .planification_dto import CoursePlanningDTO

class ChatRequest(BaseModel):
    session_id: str
    message: str
    coursePlanning: Optional[CoursePlanningDTO] = None
