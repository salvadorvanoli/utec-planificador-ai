from pydantic import BaseModel

class SuggestionResponse(BaseModel):
    analysis: str = ""
    pedagogicalSuggestions: str = ""

