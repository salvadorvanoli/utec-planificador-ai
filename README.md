# UTEC Planificador AI

**Versión:** 2.0.0

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Novedades de la Versión 2.0](#novedades-de-la-versión-20)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [API Endpoints](#api-endpoints)
6. [Seguridad](#seguridad)
7. [Base de Datos](#base-de-datos)
8. [Uso y Ejemplos](#uso-y-ejemplos)

---

## Descripción General

UTEC Planificador AI es un **microservicio de inteligencia artificial** especializado en asistencia pedagógica para planificaciones docentes de la Universidad Tecnológica del Uruguay (UTEC). Utiliza modelos de lenguaje de OpenAI (GPT-4o-mini) para proporcionar:

- **Chatbot pedagógico conversacional** con contexto de planificación
- **Generación de sugerencias** pedagógicas basadas en mejores prácticas educativas  
- **Reportes de evaluación** con análisis cualitativo de calidad pedagógica

### Contexto del Sistema

Este microservicio **NO es consumido directamente por el frontend**. Forma parte de una arquitectura de microservicios donde el backend principal Java Spring Boot (`planificador-utec-be`) actúa como orquestador:

```
Frontend → Backend Java (planificador-utec-be) → Microservicio IA (este servicio) → OpenAI API
```

**Responsabilidades del Backend Java:**
- Gestión de autenticación, autorización y sesiones de usuario
- Persistencia de entidades de dominio (planificaciones, usuarios, cursos)
- Lógica de negocio y validaciones
- Orquestación de llamadas al microservicio de IA
- Procesamiento y enriquecimiento de respuestas

**Responsabilidades de este Microservicio:**
- Análisis pedagógico mediante IA
- Procesamiento de lenguaje natural
- Gestión de contexto conversacional (temporal)
- Integración con OpenAI API

---

## Arquitectura del Sistema

### Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Frontend)                       │
│                    (Aplicación Web UTEC)                        │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/REST
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              BACKEND PRINCIPAL - Java Spring Boot               │
│                   (planificador-utec-be)                        │
│                                                                 │
│  • Autenticación y autorización                                 │
│  • Gestión de entidades (JPA/Hibernate)                         │
│  • Lógica de negocio                                            │
│  • Base de datos relacional                                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/REST (Cliente interno)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              MICROSERVICIO IA - Python FastAPI                  │
│                   (utec-planificador-ai)                        │
│                                                                 │
│  • Análisis pedagógico con IA                                   │
│  • Chatbot conversacional                                       │
│  • Generación de reportes y sugerencias                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTPS API
                               ▼
                    ┌───────────────────────┐
                    │   OpenAI API          │
                    │   (GPT-4o-mini)       │
                    └───────────────────────┘
```

### Arquitectura Interna del Microservicio

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
      │          │  + JSON Schema   │
      │          └──────────────────┘
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

## Estructura del Proyecto

```
utec-planificador-ai/
│
├── app/
│   ├── __init__.py
│   ├── main_v2.py                      # Punto de entrada FastAPI
│   │
│   ├── agents/                         # Capa de Agentes IA
│   │   ├── __init__.py
│   │   ├── chatbot_agent.py            # PedagogicalAgent (LangGraph)
│   │   └── state.py                    # ChatState (TypedDict)
│   │
│   ├── api/                            # Capa de API (Controllers)
│   │   ├── __init__.py
│   │   └── v2/                         # Endpoints versión 2
│   │       ├── __init__.py
│   │       ├── dtos/                   # Data Transfer Objects
│   │       │   ├── __init__.py
│   │       │   ├── chat_dto.py
│   │       │   ├── report_dto.py
│   │       │   └── suggestion_dto.py
│   │       └── routes/                 # Rutas REST
│   │           ├── __init__.py
│   │           ├── chatbot_routes.py
│   │           ├── report_routes.py
│   │           └── suggestion_routes.py
│   │
│   ├── core/                           # Configuración y Utilidades Core
│   │   ├── __init__.py
│   │   ├── config.py                   # Settings con Pydantic
│   │   ├── prompts.py                  # Prompts centralizados
│   │   ├── security.py                 # Validación y sanitización
│   │   └── templates/                  # Templates Jinja2 (futuro)
│   │
│   ├── database/                       # Capa de Datos
│   │   ├── __init__.py
│   │   ├── models.py                   # Modelos SQLAlchemy
│   │   └── repository.py               # ChatRepository
│   │
│   ├── services/                       # Capa de Servicios
│   │   ├── __init__.py
│   │   ├── chatbot_service.py          # Lógica de chatbot
│   │   ├── report_service.py           # Generación de reportes
│   │   └── suggestion_service.py       # Generación de sugerencias
│   │
│   └── schemas/                        # Schemas
│       ├── __init__.py
│       ├── enum_descriptions.py        # Descripciones de enums
│       ├── internal_schemas/           # Schemas Pydantic internos
│       │   ├── __init__.py
│       │   ├── report_schemas.py
│       │   └── suggestion_schemas.py
│       └── openai_schemas/             # JSON Schemas para OpenAI
│           ├── __init__.py
│           ├── report_schema.py
│           ├── suggestion_schema.py
│           └── validation_schema.py
│
├── local-scripts/                      # Scripts de utilidad
│   ├── explorar_db.py
│   ├── migrate_to_v2.py
│   ├── start_v2.bat                    # Windows
│   ├── start_v2.sh                     # Linux/Mac
│   └── verificar_db.py
│
├── scripts/                            # Scripts de deployment
│   ├── logs.ps1
│   ├── start.ps1
│   ├── status.ps1
│   └── stop.ps1
│
├── .env                                # Variables de entorno (git-ignored)
├── .env.example                        # Template de configuración
├── .gitignore
├── docker-compose.yml                  # Orquestación Docker
├── docker-compose.prod.yml             # Configuración producción
├── Dockerfile                          # Imagen Docker multi-stage
├── pyproject.toml                      # Dependencias del proyecto
├── README.md                           # Este archivo
├── EJECUCION_PROYECTO.md               # Documentación de ejecución
└── utec_planificador.db                # Base de datos SQLite (local)
```

### Descripción de Componentes

#### **Agents Layer** (`app/agents/`)
- **chatbot_agent.py:** `PedagogicalAgent` - Núcleo del sistema con LangGraph
  - Validación de relevancia educativa
  - Generación de respuestas con contexto
  - Manejo de flujos condicionales
- **state.py:** Definición de `ChatState` (TypedDict) para el grafo

#### **API Layer** (`app/api/v2/`)
- **routes/:** Endpoints REST (Controllers)
  - Validación de requests HTTP
  - Manejo de errores con HTTPException
  - Dependency injection con FastAPI Depends()
- **dtos/:** Data Transfer Objects con Pydantic
  - Validación automática de entrada
  - Serialización de respuestas

#### **Core Layer** (`app/core/`)
- **config.py:** Configuración con Pydantic Settings
  - Carga variables desde .env
  - Validación de configuración requerida
  - Singleton pattern para settings
- **prompts.py:** Templates de prompts centralizados
  - `SYSTEM_PROMPT`: Instrucciones base del asistente
  - `VALIDATION_PROMPT_TEMPLATE`: Validación de relevancia
  - `SUGGESTION_PROMPT_TEMPLATE`: Generación de sugerencias
  - `REPORT_PROMPT_TEMPLATE`: Generación de reportes
- **security.py:** Módulo de seguridad
  - Sanitización de inputs
  - Detección de SQL injection
  - Validación de session IDs
  - Logging de eventos de seguridad

#### **Database Layer** (`app/database/`)
- **models.py:** Modelos SQLAlchemy
  - `ChatMessage`: Mensajes de conversación
  - `SessionMetadata`: Metadata de sesiones
  - `Base`: Declarative base de SQLAlchemy
- **repository.py:** `ChatRepository` - Patrón Repository
  - `add_message()`: Insertar mensaje con validación
  - `get_session_messages()`: Recuperar historial
  - `delete_session()`: Eliminar sesión
  - `trim_session_messages()`: Limitar mensajes antiguos

#### **Services Layer** (`app/services/`)
- **chatbot_service.py:** `ChatbotService`
  - Orquestación del flujo de chat
  - Construcción de `ChatState`
  - Manejo de historial y contexto
- **report_service.py:** `ReportService`
  - Análisis de estadísticas y planificación
  - Generación de reportes con OpenAI
  - Parsing y validación de respuestas
- **suggestion_service.py:** `SuggestionService`
  - Análisis pedagógico de planificación
  - Generación de sugerencias accionables

#### **Schemas** (`app/schemas/`)
- **internal_schemas/:** Pydantic models para validación interna
  - Estructuras de datos del sistema
  - Response models
- **openai_schemas/:** JSON Schemas para OpenAI Structured Outputs
  - Garantizan formato de respuestas
  - Validados por OpenAI API
- **enum_descriptions.py:** Descripciones de enumeraciones
  - ODS (Objetivos de Desarrollo Sostenible)
  - Procesos cognitivos (Taxonomía de Bloom)
  - Competencias transversales
  - Estrategias de enseñanza



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
pip install .
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

El sistema implementa **6 capas de defensa en profundidad:**

#### **Capa 1: SQLAlchemy ORM**
Todas las queries usan el ORM que genera automáticamente queries parametrizadas:
```python
# ✅ Seguro: Query parametrizada automática
message = ChatMessage(session_id=session_id, content=content)
db.add(message)

# ❌ NUNCA usado: Concatenación directa
db.execute(f"INSERT INTO messages VALUES ('{session_id}', '{content}')")
```

#### **Capa 2: Módulo de Seguridad**
Validación con expresiones regulares y detección de patrones:
```python
# core/security.py
SQL_INJECTION_PATTERNS = [
    r"(\bUNION\b.*\bSELECT\b)",
    r"(\bDROP\b.*\bTABLE\b)",
    r"(\bDELETE\b.*\bFROM\b)",
    r"(;.*(-{2}|#|\\/\\*))",  # SQL comments
    # ... 15+ patrones
]
```

#### **Capa 3: Repository Layer**
Validación antes de cada operación de base de datos:
```python
# database/repository.py
def add_message(self, session_id: str, role: str, content: str):
    # Validar y sanitizar TODOS los inputs
    clean_session_id, clean_role, clean_content = validate_all_inputs(
        session_id, role, content
    )
    # Usar ORM con datos limpios
    message = ChatMessage(session_id=clean_session_id, ...)
```

#### **Capa 4: Service Layer**
Manejo de excepciones `SecurityViolation`:
```python
# services/chatbot_service.py
try:
    repo.add_message(session_id, "user", user_input)
except SecurityViolation as e:
    logger.error(f"Security violation: {e}")
    raise HTTPException(status_code=400, detail="Invalid input")
```

#### **Capa 5: API Layer**
Respuestas HTTP apropiadas sin exponer detalles internos:
```python
# api/v2/routes/chatbot_routes.py
except SecurityViolation:
    raise HTTPException(status_code=400, detail="Invalid input format")
except Exception:
    raise HTTPException(status_code=500, detail="Internal server error")
```

#### **Capa 6: Logging y Auditoría**
Registro completo de intentos de ataque:
```python
def log_security_event(event_type: str, details: dict):
    logger.warning(f"SECURITY: {event_type}", extra=details)
```

### Validación de Session IDs

**Regex de validación:**
```python
# Permitido: letras, números, guiones, guiones bajos, arroba, punto
r'^[a-zA-Z0-9._@-]+$'
```

**Formatos válidos:**
- ✅ `juan.perez@utec.edu.uy` (email)
- ✅ `550e8400-e29b-41d4-a716-446655440000` (UUID)
- ✅ `user-123` (ID simple)
- ✅ `session_abc_456` (alfanumérico)

**Formatos rechazados:**
- ❌ `user'; DROP TABLE--` (SQL injection)
- ❌ `admin' OR '1'='1` (bypass attempt)
- ❌ `<script>alert('xss')</script>` (XSS)

**Límites:**
- Longitud máxima: 255 caracteres
- Longitud mínima: 1 carácter

### Validación de Contenido

**Límites:**
- Longitud máxima por mensaje: 50,000 caracteres (50KB)
- Rol máximo: 20 caracteres

**Patrones SQL peligrosos bloqueados:**
```
DROP TABLE, DELETE FROM, UPDATE SET, INSERT INTO
UNION SELECT, EXEC, EXECUTE, xp_cmdshell
--, #, /* */, @@, INFORMATION_SCHEMA
OR 1=1, ' OR '1'='1, ' OR 'a'='a
```

**Modo educativo:** El sistema permite discutir SQL legítimamente (ejemplo: "¿Qué hace SELECT en SQL?") sin bloquear la consulta.

### Roles Permitidos

Solo se aceptan roles estándar de chat:
- `user` - Mensajes del usuario
- `assistant` - Respuestas del asistente
- `system` - Prompts del sistema (interno)

Cualquier otro valor se rechaza.

### Logging y Auditoría

**Estructura de logs de seguridad:**
```json
{
  "timestamp": "2025-12-10T12:35:30.123Z",
  "level": "WARNING",
  "event_type": "SQL_INJECTION_ATTEMPT",
  "details": {
    "session_id": "user-123",
    "pattern_detected": "DROP TABLE",
    "input_length": 156,
    "source_ip": "192.168.1.100"
  }
}
```

**Eventos registrados:**
- Intentos de SQL injection
- Session IDs inválidos
- Contenido excesivamente largo
- Roles no autorizados
- Patrones sospechosos

### Recomendaciones de Seguridad

**Para desarrollo:**
- ✅ Usar `.env` local (git-ignored)
- ✅ No compartir `OPENAI_KEY`
- ✅ Activar `DEBUG=False` en producción

**Para producción:**
- ✅ Desplegar en red privada (no exponer directamente a internet)
- ✅ Usar HTTPS (TLS/SSL)
- ✅ Variables de entorno gestionadas por plataforma (AWS Secrets Manager, Azure Key Vault)
- ✅ Implementar rate limiting (nginx, API Gateway)
- ✅ Firewall de base de datos (solo permitir conexiones desde microservicio)
- ✅ Monitoreo de logs en tiempo real
- ✅ Alertas automáticas ante patrones de ataque

---

## Base de Datos

### Esquema de Datos

El sistema utiliza dos tablas principales:

#### **chat_messages** (Mensajes de conversación)

```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_session_messages ON chat_messages(session_id, created_at);
CREATE INDEX idx_created_at ON chat_messages(created_at);
```

**Columnas:**
- `id`: Identificador único autoincremental
- `session_id`: Identificador de sesión (email, UUID, ID simple)
- `role`: Rol del mensaje (`user`, `assistant`, `system`)
- `content`: Contenido del mensaje (hasta 50KB)
- `created_at`: Timestamp de creación

**Índices:**
- `idx_session_messages`: Búsqueda rápida por sesión y orden cronológico
- `idx_created_at`: Limpieza eficiente de mensajes antiguos

#### **session_metadata** (Metadata de sesiones)

```sql
CREATE TABLE session_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message_count INTEGER DEFAULT 0
);

CREATE INDEX idx_last_activity ON session_metadata(last_activity);
```

**Columnas:**
- `id`: Identificador único
- `session_id`: Identificador de sesión (único)
- `created_at`: Fecha de creación de la sesión
- `last_activity`: Última actividad (actualizada en cada mensaje)
- `message_count`: Contador de mensajes en la sesión

**Índices:**
- `idx_last_activity`: Identificar sesiones inactivas

### Gestión de Sesiones

**Límites configurables:**
- `SESSION_MAX_MESSAGES`: Máximo de mensajes por sesión (default: 50)
- Al superar 100 mensajes, se eliminan automáticamente los 50 más antiguos

**Trimming automático:**
```python
message_limit = settings.session_max_messages  # 50
total_messages = repo.get_recent_messages_count(session_id)

if total_messages > message_limit * 2:  # 100
    repo.trim_session_messages(session_id, message_limit * 2)
```

**Ventana deslizante:** Se mantienen siempre los mensajes más recientes.

### Bases de Datos Soportadas

#### **SQLite** (Desarrollo)
```env
DATABASE_URL=sqlite:///./utec_planificador.db
```

**Ventajas:**
- ✅ Zero setup (archivo local)
- ✅ Rápido para desarrollo
- ✅ No requiere servidor

**Limitaciones:**
- ⚠️ Concurrencia limitada (1 escritor a la vez)
- ⚠️ Necesita ser cambiado en producción

#### **PostgreSQL** (Producción - Recomendado)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/utec_planificador
```

**Ventajas:**
- ✅ Concurrencia real (múltiples escrituras simultáneas)
- ✅ ACID completo
- ✅ Escalabilidad horizontal
- ✅ Respaldos automáticos
- ✅ Tipos JSON nativos
- ✅ Full-text search

**Instalación del driver:**
```bash
pip install psycopg2-binary
```

#### **MySQL** (Alternativa)
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/utec_planificador
```

**Instalación del driver:**
```bash
pip install pymysql
```

### Migración entre Bases de Datos

Gracias a SQLAlchemy ORM, cambiar de base de datos solo requiere:

1. Actualizar `DATABASE_URL` en `.env`
2. Instalar driver correspondiente
3. Reiniciar aplicación

El esquema se crea automáticamente en el primer inicio.

### Costos Estimados

**OpenAI API (GPT-4o-mini):**
- Input: $0.150 / 1M tokens
- Output: $0.600 / 1M tokens
- Promedio por conversación (10 mensajes): ~$0.02-0.05
- Costo mensual (1000 usuarios activos): ~$200-500

**Infraestructura:**
- Docker/VPS: $10-50/mes (pequeña escala)
- Kubernetes cluster: $100-300/mes (mediana escala)
- Database: $20-100/mes (PostgreSQL managed)

**Total estimado:** $230-850/mes para 1000 usuarios activos

---

## Uso y Ejemplos

### Ejemplo 1: Chatbot Conversacional

**Caso de uso:** Docente pregunta sobre metodologías de enseñanza

```bash
curl -X POST "http://localhost:8000/agent/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "docente@utec.edu.uy",
    "message": "¿Cómo puedo aplicar el aprendizaje basado en proyectos?",
    "coursePlanning": {
      "curricularUnit": {"name": "Desarrollo de Software"},
      "description": "Curso de ingeniería de software"
    }
  }'
```

**Respuesta esperada:**
```json
{
  "reply": "El Aprendizaje Basado en Proyectos (ABP) es una metodología muy efectiva para tu curso de Desarrollo de Software. Aquí te propongo algunos pasos:

1. **Define un proyecto real**: Puede ser una aplicación web completa, una API REST, o un sistema de gestión.

2. **Establece hitos semanales**: 
   - Semana 1-2: Análisis y diseño
   - Semana 3-4: Implementación del backend
   - Semana 5-6: Frontend e integración
   - Semana 7-8: Testing y despliegue

3. **Trabajo en equipos**: Asigna roles (Product Owner, Scrum Master, Developers) para simular entornos profesionales.

4. **Evaluación continua**: Revisiones de sprint cada 2 semanas con retroalimentación.

5. **Vinculación con ODS**: Puedes proponer proyectos que aborden problemas sociales (ODS 4: Educación, ODS 8: Trabajo decente).

¿Te gustaría que profundice en algún aspecto específico?"
}
```

### Ejemplo 2: Generar Sugerencias

```bash
curl -X POST "http://localhost:8000/agent/suggestions" \
  -H "Content-Type: application/json" \
  -d @planificacion.json
```

**planificacion.json:**
```json
{
  "coursePlanning": {
    "curricularUnit": {
      "name": "Algoritmos y Estructura de Datos",
      "credits": 8
    },
    "description": "Curso fundamental de algoritmos",
    "weeklyPlannings": [
      {
        "weekNumber": 1,
        "activities": [
          {
            "name": "Introducción a algoritmos",
            "cognitiveProcesses": ["REMEMBER", "UNDERSTAND"],
            "teachingStrategies": ["LECTURE"]
          }
        ]
      }
    ]
  }
}
```

### Ejemplo 3: Generar Reporte

```python
import requests

url = "http://localhost:8000/agent/report/generate"

payload = {
    "courseId": "curso-123",
    "statistics": {
        "cognitiveProcesses": {
            "REMEMBER": 5,
            "UNDERSTAND": 10,
            "APPLY": 15,
            "ANALYZE": 8,
            "EVALUATE": 4,
            "CREATE": 3
        },
        "totalWeeks": 16,
        "totalInPersonHours": 96,
        "totalVirtualHours": 48,
        "totalHybridHours": 24
    },
    "coursePlanning": {
        "curricularUnit": {"name": "Inteligencia Artificial"},
        "description": "Curso avanzado de IA"
    }
}

response = requests.post(url, json=payload)
report = response.json()

print(f"Análisis: {report['report']['detailedAnalysis']['cognitiveProcesses']}")
print(f"Fortalezas: {report['report']['strengths']}")
print(f"Mejoras: {report['report']['improvementAreas']}")
```

---

**Docstrings:**
```python
def generate_report(course_id: str, statistics: Dict) -> ReportResponse:
    """
    Generate a pedagogical evaluation report.
    
    Args:
        course_id: Unique identifier for the course
        statistics: Dictionary with course statistics
        
    Returns:
        ReportResponse with analysis and recommendations
        
    Raises:
        HTTPException: If validation fails or OpenAI error occurs
    """
    pass
```

### Documentación

- **README.md:** Documentación principal (este archivo)
- **Docstrings:** En todas las funciones públicas
- **OpenAPI:** Generada automáticamente en `/docs`

---
