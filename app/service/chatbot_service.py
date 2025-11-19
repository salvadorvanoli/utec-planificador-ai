from ..graph.chatbot_graph import ReactAgentWrapper
from ..graph.utils import session_memory_store
from ..graph.schema.chat_state import ChatState

session_store = {}

chatbot_graph = ReactAgentWrapper()


def run_chatbot(session_id: str, user_message: str, planning: dict = None) -> str:
    state = ChatState(
        session_id=session_id,
        input=user_message,
        history=[],
        planning=planning
    )

    result_dict = chatbot_graph.invoke(state)

    reply = result_dict.get("reply")
    if not reply:
        raise RuntimeError("There was no reply from the bot")

    session_store[session_id] = "active"

    return reply


def clear_chat_session(session_id: str) -> bool:
    if session_id in session_memory_store:
        del session_memory_store[session_id]
        return True
    return False
