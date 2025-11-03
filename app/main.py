from fastapi import FastAPI
from app.api.chatbot_controller import router as chat_router
from app.api.suggestion_controller import router as suggestion_router
from app.api.report_controller import router as report_router

app = FastAPI(
    title="UTEC Planificador AI Agent",
    description="Asistente Pedagógico con IA para el Planificador Docente de UTEC",
    version="0.1.0"
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
