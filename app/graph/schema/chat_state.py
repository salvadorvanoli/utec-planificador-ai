from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ChatState:
    session_id: str
    input: str
    history: List[Dict[str, Any]] = field(default_factory=list)

