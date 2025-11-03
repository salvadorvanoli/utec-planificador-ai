from pydantic import BaseModel

class SuggestionResponse(BaseModel):
    analysis: str = ""
    pedagogical_suggestions: str = ""
