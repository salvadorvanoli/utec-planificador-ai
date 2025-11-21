from datetime import datetime, timedelta
import threading
import time
import logging

logger = logging.getLogger(__name__)

session_memory_store = {}
SESSION_TIMEOUT_MINUTES = 20
CLEANUP_INTERVAL_SECONDS = 300  # Ejecutar limpieza cada 5 minutos

class InMemoryHistory:
    def __init__(self):
        self.messages = []

    def add_messages(self, messages: list) -> None:
        self.messages.extend(messages)

    def get_messages(self) -> list:
        return self.messages

    def clear(self) -> None:
        self.messages = []


def cleanup_expired_sessions():
    """Elimina sesiones expiradas del almacenamiento en memoria"""
    current_time = datetime.now()
    expired_sessions = [
        sid for sid, (history, timestamp) in session_memory_store.items()
        if current_time - timestamp > timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    ]
    for sid in expired_sessions:
        del session_memory_store[sid]
        logger.info(f"Sesión expirada eliminada: {sid}")

    if expired_sessions:
        logger.info(f"Limpieza completada: {len(expired_sessions)} sesión(es) eliminada(s)")


def background_cleanup_task():
    """Tarea en segundo plano que limpia sesiones expiradas periódicamente"""
    while True:
        try:
            time.sleep(CLEANUP_INTERVAL_SECONDS)
            cleanup_expired_sessions()
        except Exception as e:
            logger.error(f"Error en limpieza automática de sesiones: {e}")


def start_cleanup_thread():
    """Inicia el thread de limpieza en segundo plano"""
    cleanup_thread = threading.Thread(target=background_cleanup_task, daemon=True)
    cleanup_thread.start()
    logger.info(f"Thread de limpieza automática iniciado (cada {CLEANUP_INTERVAL_SECONDS}s)")


def get_or_create_history(session_id: str) -> InMemoryHistory:
    current_time = datetime.now()
    # Limpieza sincrónica adicional al acceder
    cleanup_expired_sessions()

    if session_id not in session_memory_store:
        session_memory_store[session_id] = (InMemoryHistory(), current_time)
        logger.info(f"Nueva sesión creada: {session_id}")
    else:
        history, _ = session_memory_store[session_id]
        session_memory_store[session_id] = (history, current_time)

    return session_memory_store[session_id][0]


# Iniciar el thread de limpieza automática al importar el módulo
start_cleanup_thread()


