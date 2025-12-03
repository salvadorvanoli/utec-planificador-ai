# ============================================
# Build Stage - Dependency Installation
# ============================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias de sistema necesarias para compilar paquetes
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        libpq-dev \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY pyproject.toml ./

# Crear entorno virtual e instalar dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Actualizar pip y setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instalar dependencias del proyecto
RUN pip install --no-cache-dir \
    fastapi>=0.104.0 \
    uvicorn[standard]>=0.24.0 \
    openai>=1.0.0 \
    python-dotenv>=1.0.0 \
    langgraph>=0.0.20 \
    langchain>=0.1.0 \
    langchain-core>=0.1.0 \
    langchain-openai>=0.0.2 \
    loguru>=0.7.0 \
    pydantic>=2.0.0

# ============================================
# Runtime Stage - Production Image
# ============================================
FROM python:3.12-slim AS runtime

# Metadatos de la imagen
LABEL maintainer="UTEC Planificador Team"
LABEL description="AI Agent Microservice del Planificador Docente - FastAPI + OpenAI"
LABEL version="1.0.0"
LABEL org.opencontainers.image.title="UTEC Planificador AI Agent"
LABEL org.opencontainers.image.description="Microservicio de IA para asistencia pedagógica y análisis de planificaciones"
LABEL org.opencontainers.image.vendor="Universidad Tecnológica del Uruguay"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/joaqui-jz/utec-planificador-ai"

# Instalar dependencias runtime mínimas
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar timezone
ENV TZ=America/Montevideo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Crear usuario no-root para seguridad
RUN groupadd -r aiagent && useradd -r -g aiagent aiagent

# Establecer directorio de trabajo
WORKDIR /app

# Copiar entorno virtual desde builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar código de la aplicación
COPY --chown=aiagent:aiagent app/ ./app/
COPY --chown=aiagent:aiagent main.py ./

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Cambiar a usuario no-root
USER aiagent

# Exponer puerto de la aplicación
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
