from pydantic import BaseModel
from typing import Optional
from .planification_dto import CoursePlanningDTO

class ChatRequest(BaseModel):
    session_id: str
    message: str
    coursePlanning: Optional[CoursePlanningDTO] = None
