from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.api.chatbot_controller import router as chat_router
from app.api.suggestion_controller import router as suggestion_router
from app.api.report_controller import router as report_router

# Configurar logging para toda la aplicación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("=== UTEC Planificador AI Agent iniciado ===")
    logger.info("Sistema de limpieza automática de sesiones activo")
    from app.graph.utils import SESSION_TIMEOUT_MINUTES, CLEANUP_INTERVAL_SECONDS
    logger.info(f"Configuración: Timeout={SESSION_TIMEOUT_MINUTES}min, Limpieza cada={CLEANUP_INTERVAL_SECONDS}s")
    yield
    # Shutdown
    logger.info("=== UTEC Planificador AI Agent detenido ===")

app = FastAPI(
    title="UTEC Planificador AI Agent",
    description="Asistente Pedagógico con IA para el Planificador Docente de UTEC",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(chat_router, prefix="/agent")
app.include_router(suggestion_router, prefix="/agent")
app.include_router(report_router, prefix="/agent")

@app.get("/")
async def root():
    return {
        "message": "UTEC Planificador AI Agent",
        "status": "online",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
