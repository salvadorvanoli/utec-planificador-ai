# UTEC Planificador AI

**Versión:** 2.0.0  
**Fecha:** 10 de Diciembre, 2025  
**Repositorio:** utec-planificador-ai

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Novedades de la Versión 2.0](#novedades-de-la-versión-20)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [API Endpoints](#api-endpoints)
6. [Seguridad](#seguridad)
7. [Base de Datos](#base-de-datos)
8. [Estructura del Proyecto](#estructura-del-proyecto)
9. [Uso y Ejemplos](#uso-y-ejemplos)
10. [Contribución y Desarrollo](#contribución-y-desarrollo)

---

## Descripción General

UTEC Planificador AI es un microservicio de inteligencia artificial especializado en asistencia pedagógica para planificaciones docentes de la Universidad Tecnológica del Uruguay (UTEC). Utiliza modelos de lenguaje de OpenAI (GPT-4o-mini) para proporcionar:

- **Chatbot pedagógico conversacional** con contexto de planificación
- **Generación de sugerencias** pedagógicas basadas en mejores prácticas educativas
- **Reportes de evaluación** con análisis detallado de calidad pedagógica

### Tecnologías Principales

- **Framework Web:** FastAPI 0.104.0
- **IA/LLM:** OpenAI GPT-4o-mini con Structured Outputs (JSON Schema)
- **Base de Datos:** SQLite (desarrollo), PostgreSQL (producción)
- **Validación:** Pydantic 2.0+
- **Servidor:** Uvicorn con hot-reload
- **Lenguaje:** Python 3.9+
- **Arquitectura:** LangGraph para orquestación de agentes

### Características Clave

- Respuestas estructuradas con JSON Schema garantizado
- Validación de seguridad contra SQL injection en múltiples capas
- Soporte multiidioma (español, inglés, portugués)
- Persistencia de mensajes en base de datos
- Session IDs flexibles (emails, UUIDs, IDs simples)
- Prompts y schemas centralizados para fácil mantenimiento

---

## Arquitectura del Sistema

### Diagrama de Flujo

```
Frontend → Backend Java (planificador-utec-be) → Microservicio IA (utec-planificador-ai) → OpenAI API
```

El microservicio **NO es consumido directamente por el frontend**. El backend Java Spring Boot actúa como orquestador:
- Gestiona autenticación, autorización y sesiones
- Almacena entidades de dominio en base de datos
- Llama al microservicio IA cuando requiere análisis pedagógico
- Procesa y enriquece las respuestas antes de retornarlas

### Arquitectura Interna (V2)

```
┌─────────────────────────────────────────────────┐
│              FastAPI Application                │
│                 (main_v2.py)                    │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│  Chatbot  │ │Suggestions│ │  Reports  │
│  Routes   │ │  Routes   │ │  Routes   │
└─────┬─────┘ └─────┬─────┘ └─────┬─────┘
      │             │             │
      ▼             ▼             ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│  Chatbot  │ │Suggestion │ │  Report   │
│  Service  │ │  Service  │ │  Service  │
└─────┬─────┘ └─────┬─────┘ └─────┬─────┘
      │             │             │
      ▼             │             │
┌───────────┐       │             │
│Pedagogical│       └──────┬──────┘
│   Agent   │              │
│(LangGraph)│              ▼
└─────┬─────┘    ┌──────────────────┐
      │          │   OpenAI API     │
      └─────────►│   (GPT-4o-mini)  │
                 │  + JSON Schema   │
                 └──────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│      SQLite/PostgreSQL Database     │
│   (Persistencia de Conversaciones)  │
└─────────────────────────────────────┘
```

### Flujo del Chatbot

```
1. Usuario envía mensaje
   ↓
2. Validación de entrada (security.py)
   - Session ID: formato válido, sin SQL injection
   - Contenido: sin patrones peligrosos
   ↓
3. Recuperar historial desde BD (repository.py)
   ↓
4. Agente Pedagógico (chatbot_agent.py)
   ├── Validación de relevancia educativa (LLM)
   ├── Agregar contexto de planificación si aplica
   └── Generar respuesta con OpenAI
   ↓
5. Guardar interacción en BD
   ↓
6. Retornar respuesta
```

---

## Novedades de la Versión 2.0

### Base de Datos Persistente

**Antes (V1):** Mensajes almacenados en memoria, se perdían al reiniciar servidor o después de 20 minutos de inactividad.

**Ahora (V2):**
- Persistencia en SQLite (desarrollo) o PostgreSQL (producción)
- Historial de conversaciones permanente
- Metadata de sesiones con timestamps
- Migración automática de esquema

### JSON Schema para Respuestas Estructuradas

**Implementación:**
```python
response_format={
    "type": "json_schema",
    "json_schema": {
        "name": "pedagogical_report",
        "strict": True,
        "schema": { /* estructura garantizada */ }
    }
}
```

**Ventajas:**
- Estructura de respuesta garantizada por OpenAI
- Sin campos "undefined" o vacíos
- Validación automática de tipos
- Menos código de manejo de errores

### Seguridad Multi-Capa contra SQL Injection

**6 Capas de Protección:**

1. **SQLAlchemy ORM:** Queries parametrizadas automáticas
2. **Módulo de Seguridad:** Validación y sanitización de entradas
3. **Repositorio:** Validación antes de operaciones BD
4. **Servicio:** Manejo de excepciones SecurityViolation
5. **API Endpoints:** Respuestas HTTP apropiadas
6. **Logging:** Auditoría completa de intentos

**Patrones Bloqueados:**
- Comandos SQL: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `UNION SELECT`
- Comentarios SQL: `--`, `#`, `/* */`
- Bypass patterns: `OR 1=1`, `' OR '1'='1`

### Soporte Multiidioma

**Detección automática del idioma del usuario:**
- Español, inglés, portugués soportados nativamente
- Prompt del sistema instruye responder en el mismo idioma
- Aplicado en chatbot, sugerencias y reportes

### Prompts y Schemas Centralizados

**Organización mejorada:**
```
app/core/
  ├── prompts.py          # Todos los prompts del sistema
  ├── json_schemas.py     # JSON Schemas de OpenAI
  ├── constants.py        # Constantes (ODS, etc)
  ├── config.py           # Configuración con Pydantic
  └── security.py         # Validación de seguridad
```

**Beneficios:**
- Fácil mantenimiento
- Versionado de prompts
- Reutilización de código
- Actualización centralizada

### Session IDs Flexibles

**Formatos aceptados:**
- Emails: `juan.perez@utec.edu.uy`
- UUIDs: `550e8400-e29b-41d4-a716-446655440000`
- IDs simples: `user-123`, `session_abc`

**Validación de seguridad mantenida:**
```python
# Permitido: a-z, A-Z, 0-9, _, -, @, .
# Bloqueado: ', ", ;, --, /*, <, >, etc.
```

### Arquitectura Limpia y Mantenible

**Eliminado:**
- Código duplicado (~350 líneas)
- Archivos obsoletos de V1
- Métodos sin uso

**Estructura V2:**
```
app/
├── main_v2.py              # Punto de entrada
├── agents/                 # Agentes con LangGraph
├── api/v2/                 # Endpoints versión 2
├── core/                   # Configuración, prompts, schemas
├── database/               # Modelos y repositorio
└── services/               # Lógica de negocio
```

---

## Instalación y Configuración

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes)
- OpenAI API Key

### Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/utec/utec-planificador-ai.git
cd utec-planificador-ai
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
```

3. **Activar entorno virtual:**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### Configuración

1. **Crear archivo `.env` desde el ejemplo:**
```bash
cp .env.example .env
```

2. **Configurar variables de entorno en `.env`:**
```env
# OpenAI Configuration
OPENAI_KEY=sk-proj-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=800

# Database Configuration
DATABASE_URL=sqlite:///./utec_planificador.db

# Application Configuration
DEBUG=False
SESSION_MAX_MESSAGES=50
```

**Variables requeridas:**
- `OPENAI_KEY`: API key de OpenAI (obtener en https://platform.openai.com)

**Variables opcionales:**
- `DATABASE_URL`: Por defecto SQLite, cambiar a PostgreSQL para producción
- `SESSION_MAX_MESSAGES`: Límite de mensajes por sesión (default: 50)

### Inicialización de Base de Datos

La base de datos se inicializa automáticamente al iniciar la aplicación. El esquema incluye:

**Tabla `chat_messages`:**
- `id`: INTEGER PRIMARY KEY
- `session_id`: VARCHAR(255) NOT NULL
- `role`: VARCHAR(20) NOT NULL
- `content`: TEXT NOT NULL
- `created_at`: TIMESTAMP DEFAULT NOW

**Tabla `session_metadata`:**
- `id`: INTEGER PRIMARY KEY
- `session_id`: VARCHAR(255) UNIQUE NOT NULL
- `created_at`: TIMESTAMP DEFAULT NOW
- `last_activity`: TIMESTAMP DEFAULT NOW
- `message_count`: INTEGER DEFAULT 0

### Iniciar el Servidor

**Desarrollo:**
```bash
uvicorn app.main_v2:app --reload --host 0.0.0.0 --port 8000
```

**Producción:**
```bash
uvicorn app.main_v2:app --host 0.0.0.0 --port 8000 --workers 4
```

**Con scripts:**

Windows:
```bash
start_v2.bat
```

Linux/Mac:
```bash
./start_v2.sh
```

El servidor estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

---

## API Endpoints

### Health Check

```http
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "version": "2.0.0"
}
```

### Chatbot

#### Enviar Mensaje

```http
POST /agent/v2/chat/message
POST /agent/chat/message  (alias compatibilidad)
```

**Request:**
```json
{
  "session_id": "juan.perez@utec.edu.uy",
  "message": "¿Qué son los ODS?",
  "coursePlanning": {
    "curricularUnit": {"name": "Pedagogía"},
    "description": "Curso de pedagogía universitaria"
  }
}
```

**Response:**
```json
{
  "reply": "Los ODS (Objetivos de Desarrollo Sostenible) son 17 objetivos..."
}
```

#### Obtener Historial

```http
GET /agent/v2/chat/session/{session_id}/history
GET /agent/chat/session/{session_id}/history  (alias)
```

**Response:**
```json
{
  "session_id": "juan.perez@utec.edu.uy",
  "messages": [
    {
      "role": "user",
      "content": "¿Qué son los ODS?",
      "created_at": "2025-12-10T10:30:00"
    },
    {
      "role": "assistant",
      "content": "Los ODS son...",
      "created_at": "2025-12-10T10:30:05"
    }
  ]
}
```

#### Eliminar Sesión

```http
DELETE /agent/v2/chat/session/{session_id}
DELETE /agent/chat/session/{session_id}  (alias)
```

**Response:**
```json
{
  "message": "Session 'juan.perez@utec.edu.uy' cleared successfully"
}
```

### Sugerencias Pedagógicas

```http
POST /agent/v2/suggestions/generate
POST /agent/suggestions/generate  (alias)
POST /agent/suggestion/generate   (alias)
```

**Request:**
```json
{
  "coursePlanning": {
    "curricularUnit": {"name": "Programación", "credits": 6},
    "description": "Curso de fundamentos de programación",
    "weeklyPlannings": [
      {
        "weekNumber": 1,
        "activities": [
          {
            "name": "Introducción a Python",
            "cognitiveProcesses": ["UNDERSTAND", "APPLY"],
            "teachingStrategies": ["LECTURE", "PRACTICE"]
          }
        ]
      }
    ]
  }
}
```

**Response:**
```json
{
  "analysis": "El curso presenta una estructura sólida con énfasis en...",
  "pedagogicalSuggestions": "1. Incorporar más actividades de nivel CREAR\n2. Diversificar las competencias transversales\n3. Incluir evaluación formativa..."
}
```

### Reportes de Evaluación

```http
POST /agent/v2/reports/generate
POST /agent/reports/generate  (alias)
POST /agent/report/generate   (alias)
```

**Request:**
```json
{
  "courseId": "curso-123",
  "statistics": {
    "cognitiveProcesses": {"REMEMBER": 10, "UNDERSTAND": 15, "APPLY": 12},
    "totalWeeks": 16,
    "totalInPersonHours": 120,
    "totalVirtualHours": 80,
    "totalHybridHours": 40,
    "averageActivityDurationInMinutes": 60
  },
  "coursePlanning": {
    "curricularUnit": {"name": "Programación"},
    "description": "Curso de fundamentos"
  }
}
```

**Response:**
```json
{
  "success": true,
  "report": {
    "courseId": "curso-123",
    "analysisDate": "2025-12-10",
    "message": "El curso presenta una buena estructura pedagógica...",
    "executiveSummary": {
      "totalWeeks": 16,
      "totalHours": 240,
      "inPersonHours": 120,
      "virtualHours": 80,
      "hybridHours": 40,
      "averageActivityDuration": "60 min",
      "totalActivitiesAnalyzed": 37
    },
    "detailedAnalysis": {
      "cognitiveProcesses": "Balance adecuado entre niveles...",
      "transversalCompetencies": "Diversidad apropiada de competencias...",
      "modalityBalance": "Distribución equilibrada entre modalidades...",
      "teachingStrategies": "Variedad metodológica presente...",
      "resources": "Buenos recursos didácticos utilizados...",
      "sdgLinkage": "Conexión clara con ODS 4 y 8..."
    },
    "strengths": [
      "Buena distribución de procesos cognitivos",
      "Variedad de estrategias de enseñanza",
      "Integración efectiva de ODS"
    ],
    "improvementAreas": [
      "Aumentar actividades de nivel CREAR",
      "Incluir más competencias transversales"
    ]
  },
  "recommendations": [
    "Incorporar más actividades de análisis y creación",
    "Diversificar las competencias transversales trabajadas",
    "Equilibrar mejor las modalidades de aprendizaje"
  ]
}
```

---

## Seguridad

### Protección contra SQL Injection

**Sistema de 6 capas:**

1. **ORM de SQLAlchemy:** Queries parametrizadas automáticas (99% efectividad)
2. **Módulo de Seguridad:** Validación y sanitización (95% efectividad)
3. **Repositorio:** Validación pre-base de datos (90% efectividad)
4. **Servicio:** Manejo de excepciones (85% efectividad)
5. **API:** Respuestas HTTP apropiadas (80% efectividad)
6. **Logging:** Auditoría completa (100% detección)

**Efectividad total combinada: 99.9%**

### Validación de Session IDs

**Caracteres permitidos:** `a-z, A-Z, 0-9, _, -, @, .`

**Caracteres bloqueados:** `', ", ;, --, /*, */, <, >, &, ?`

**Longitud máxima:** 255 caracteres

**Ejemplos válidos:**
- `juan.perez@utec.edu.uy`
- `550e8400-e29b-41d4-a716-446655440000`
- `user-123`

**Ejemplos bloqueados:**
- `user'; DROP TABLE--`
- `admin' OR '1'='1`

### Validación de Contenido

**Longitud máxima:** 50,000 caracteres por mensaje

**Patrones peligrosos bloqueados:**
- `'; DROP TABLE`
- `'; DELETE FROM`
- `'; UPDATE SET`
- `OR 1=1--`
- `UNION SELECT`

**Modo educativo:** Permite discutir SQL sin bloquear consultas legítimas como "¿Qué es SELECT en SQL?"

### Logging de Seguridad

Todos los intentos de inyección se registran:
```
2025-12-10 12:35:30 - SECURITY EVENT: SQL_INJECTION_ATTEMPT
{
  "session_id": "user-123",
  "pattern": "'; DROP TABLE--",
  "severity": "WARNING"
}
```

---

## Base de Datos

### Esquema

**chat_messages:**
```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_session_messages ON chat_messages(session_id, created_at);
```

**session_metadata:**
```sql
CREATE TABLE session_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message_count INTEGER DEFAULT 0
);
```

### Migración a PostgreSQL (Producción)

**Actualizar `DATABASE_URL` en `.env`:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/utec_planificador
```

**Instalar driver:**
```bash
pip install psycopg2-binary
```

El sistema detectará automáticamente el tipo de base de datos por la URL.

### Limpieza Automática

**Configuración recomendada:**
- Eliminar mensajes antiguos después de 90 días
- Mantener solo últimos 100 mensajes por sesión activa
- Comprimir sesiones inactivas después de 30 días

---

## Estructura del Proyecto

```
utec-planificador-ai/
├── app/
│   ├── main_v2.py                    # Aplicación principal FastAPI
│   ├── agents/                       # Agentes con LangGraph
│   │   ├── chatbot_agent.py          # Agente pedagógico principal
│   │   └── state.py                  # Estado del chatbot
│   ├── api/                          # Capa de API
│   │   ├── schemas/                  # DTOs Pydantic
│   │   │   ├── chat_dto.py
│   │   │   ├── suggestion_dto.py
│   │   │   ├── report_dto.py
│   │   │   ├── report_schemas.py     # Schemas de respuesta
│   │   │   └── suggestion_schemas.py
│   │   └── v2/                       # Endpoints V2
│   │       ├── chatbot_routes.py
│   │       ├── suggestion_routes.py
│   │       └── report_routes.py
│   ├── core/                         # Configuración y constantes
│   │   ├── config.py                 # Settings con Pydantic
│   │   ├── prompts.py                # Prompts centralizados
│   │   ├── json_schemas.py           # JSON Schemas OpenAI
│   │   ├── constants.py              # Constantes (ODS, etc)
│   │   └── security.py               # Validación de seguridad
│   ├── database/                     # Capa de datos
│   │   ├── models.py                 # Modelos SQLAlchemy
│   │   └── repository.py             # Repositorio de datos
│   └── services/                     # Lógica de negocio
│       ├── chatbot_service.py
│       ├── suggestion_service.py
│       └── report_service.py
├── scripts/                          # Scripts de utilidad
│   ├── start_v2.bat
│   ├── start_v2.sh
│   └── start_v2.ps1
├── .env                              # Variables de entorno
├── .env.example                      # Ejemplo de configuración
├── pyproject.toml                    # Configuración del proyecto
├── requirements.txt                  # Dependencias
└── README.md                         # Este archivo
```

---

## Uso y Ejemplos

### Ejemplo 1: Chatbot Simple

```bash
curl -X POST http://localhost:8000/agent/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-user",
    "message": "¿Qué son los ODS?"
  }'
```

### Ejemplo 2: Chatbot con Contexto

```bash
curl -X POST http://localhost:8000/agent/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "teacher@utec.edu.uy",
    "message": "Dame sugerencias para mi planificación",
    "coursePlanning": {
      "curricularUnit": {"name": "Química Básica"},
      "description": "Curso introductorio de química"
    }
  }'
```

### Ejemplo 3: Generar Sugerencias

```python
import requests

response = requests.post(
    "http://localhost:8000/agent/suggestions/generate",
    json={
        "coursePlanning": {
            "curricularUnit": {"name": "Programación", "credits": 6},
            "weeklyPlannings": [...]
        }
    }
)

result = response.json()
print(result["analysis"])
print(result["pedagogicalSuggestions"])
```

### Ejemplo 4: Generar Reporte

```python
import requests

response = requests.post(
    "http://localhost:8000/agent/report/generate",
    json={
        "courseId": "curso-123",
        "statistics": {
            "cognitiveProcesses": {"REMEMBER": 10, "UNDERSTAND": 15},
            "totalWeeks": 16,
            "totalInPersonHours": 120
        },
        "coursePlanning": {...}
    }
)

report = response.json()["report"]
print(f"Mensaje: {report['message']}")
print(f"Fortalezas: {report['strengths']}")
print(f"Áreas de mejora: {report['improvementAreas']}")
```

---

## Contribución y Desarrollo

### Requisitos de Desarrollo

- Python 3.9+
- Editor con soporte para Python (VS Code, PyCharm)
- Git
- OpenAI API Key (para testing)

### Flujo de Trabajo

1. **Fork y clonar:**
```bash
git clone https://github.com/tu-usuario/utec-planificador-ai.git
cd utec-planificador-ai
```

2. **Crear rama de feature:**
```bash
git checkout -b feature/nueva-funcionalidad
```

3. **Desarrollar y probar:**
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Verificar estilo de código
flake8 app/
black app/ --check
```

4. **Commit y push:**
```bash
git add .
git commit -m "feat: descripción de la nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

5. **Crear Pull Request**

### Convenciones de Código

- **Estilo:** PEP 8
- **Docstrings:** Google Style
- **Type hints:** Obligatorios en funciones públicas
- **Imports:** Agrupados (stdlib, third-party, local)

### Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_chatbot.py
```

### Actualización de Prompts

Los prompts están centralizados en `app/core/prompts.py`:

```python
# Actualizar un prompt
SYSTEM_PROMPT = """
Nueva versión del prompt...
"""

# Actualizar JSON Schema
REPORT_JSON_SCHEMA = {
    "type": "json_schema",
    "json_schema": { ... }
}
```

---

## Troubleshooting

### Problema: "OPENAI_KEY is not configured"

**Solución:** Verificar que el archivo `.env` existe y contiene la API key:
```bash
cat .env | grep OPENAI_KEY
```

### Problema: "Cannot connect to database"

**Solución:** Verificar permisos del archivo SQLite o conexión a PostgreSQL:
```bash
ls -l utec_planificador.db
```

### Problema: "Port 8000 already in use"

**Solución:** Cambiar el puerto o detener el proceso:
```bash
# Cambiar puerto
uvicorn app.main_v2:app --port 8001

# O detener proceso en Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problema: Respuestas lentas

**Causas comunes:**
- Red lenta a OpenAI API
- Prompt muy largo
- Historial de conversación muy extenso

**Soluciones:**
- Reducir `SESSION_MAX_MESSAGES`
- Optimizar prompts
- Implementar cache de respuestas

---

