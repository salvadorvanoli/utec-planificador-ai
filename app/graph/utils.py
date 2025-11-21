from datetime import datetime, timedelta

session_memory_store = {}

class InMemoryHistory:
    def __init__(self):
        self.messages = []

    def add_messages(self, messages: list) -> None:
        self.messages.extend(messages)

    def get_messages(self) -> list:
        return self.messages

    def clear(self) -> None:
        self.messages = []


def get_or_create_history(session_id: str) -> InMemoryHistory:
    current_time = datetime.now()
    expired_sessions = [
        sid for sid, (history, timestamp) in session_memory_store.items()
        if current_time - timestamp > timedelta(minutes=20)
    ]
    for sid in expired_sessions:
        del session_memory_store[sid]
    if session_id not in session_memory_store:
        session_memory_store[session_id] = (InMemoryHistory(), current_time)
    else:
        history, _ = session_memory_store[session_id]
        session_memory_store[session_id] = (history, current_time)
    return session_memory_store[session_id][0]

