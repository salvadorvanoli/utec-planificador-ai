"""UTEC Planificador AI - Main Application (V2)"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.database.models import init_database
from app.api.v2.routes.chatbot_routes import router as chatbot_router
from app.api.v2.routes.suggestion_routes import router as suggestion_router
from app.api.v2.routes.report_routes import router as report_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    logger.info("=" * 60)
    logger.info("UTEC Planificador AI Agent V2 - Starting")
    logger.info("=" * 60)

    settings = get_settings()
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Database: {settings.database_url}")

    # Initialize database
    logger.info("Initializing database...")
    init_database()
    logger.info("Database initialized successfully")

    logger.info("Application ready")
    logger.info("=" * 60)

    yield

    logger.info("=" * 60)
    logger.info("UTEC Planificador AI Agent V2 - Shutting down")
    logger.info("=" * 60)


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Asistente Pedagógico con IA para el Planificador Docente de UTEC. "
        "Versión 2.0 con arquitectura mejorada, LangGraph y persistencia en base de datos."
    ),
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router, prefix="/agent")
app.include_router(suggestion_router, prefix="/agent")
app.include_router(report_router, prefix="/agent")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "UTEC Planificador AI Agent",
        "version": settings.app_version,
        "status": "online",
        "api_version": "v2",
        "description": "Asistente pedagógico con IA para planificación docente"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


@app.get("/version")
async def version():
    """Version information endpoint."""
    return {
        "version": settings.app_version,
        "api_version": "v2",
        "features": [
            "LangGraph-based agent architecture",
            "Database persistence for chat history",
            "Improved prompt management",
            "Modular service layer",
            "Enhanced error handling"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_v2:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )

