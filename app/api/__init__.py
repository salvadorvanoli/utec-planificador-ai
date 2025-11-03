from .chatbot_controller import router as chatbot_router
from .suggestion_controller import router as suggestion_router
from .report_controller import router as report_router

__all__ = ["chatbot_router", "suggestion_router", "report_router"]
