# 📚 UTEC Planificador AI - Documentación Completa

**Versión:** 0.1.0  
**Fecha:** 26 de Noviembre, 2025  
**Repositorio:** utec-planificador-ai

---

## 📋 Tabla de Contenidos

1. [Descripción General](#-descripción-general)
2. [Arquitectura del Sistema](#-arquitectura-del-sistema)
3. [Infraestructura y Componentes](#-infraestructura-y-componentes)
4. [Endpoints de la API](#-endpoints-de-la-api)
5. [Sistema de Seguridad](#-sistema-de-seguridad)
6. [Gestión de Sesiones](#-gestión-de-sesiones)
7. [Modelos de Datos](#-modelos-de-datos)
8. [Configuración e Instalación](#-configuración-e-instalación)
9. [Casos de Uso](#-casos-de-uso)

---

## 🎯 Descripción General

### ¿Qué es UTEC Planificador AI?

**UTEC Planificador AI** es un microservicio de inteligencia artificial especializado que actúa como motor de análisis pedagógico para el sistema principal **planificador-utec-be** (Java Spring Boot). Este microservicio utiliza modelos de lenguaje de OpenAI (GPT-4o-mini) para proporcionar:

- **Asistencia pedagógica conversacional** mediante un chatbot especializado
- **Análisis profundo de planificaciones** con sugerencias basadas en mejores prácticas educativas
- **Generación de reportes** con evaluación de calidad pedagógica

### Arquitectura de Integración

Este microservicio **NO es consumido directamente por el frontend**. El flujo correcto es:

```
Frontend → Backend Java (planificador-utec-be) → Microservicio IA (utec-planificador-ai) → OpenAI API
```

El backend Java Spring Boot:
- Gestiona toda la lógica de negocio
- Maneja autenticación, autorización y sesiones de usuario
- Almacena y consulta entidades en base de datos
- Orquesta las llamadas al microservicio de IA cuando se requiere análisis pedagógico
- Procesa y enriquece las respuestas de IA antes de retornarlas al frontend

### Propósito

El sistema está diseñado para:
- Mejorar la calidad de las planificaciones docentes
- Promover la aplicación de principios pedagógicos modernos (UDL, Taxonomía de Bloom revisada)
- Facilitar la alineación con Objetivos de Desarrollo Sostenible (ODS)
- Proporcionar retroalimentación constructiva basada en estándares educativos internacionales
- **Separar la lógica de IA del backend principal**, permitiendo escalabilidad independiente

### Tecnologías Principales

- **Framework Web:** FastAPI 0.104.0+
- **IA/LLM:** OpenAI GPT-4o-mini
- **Validación de Datos:** Pydantic 2.0+
- **Servidor:** Uvicorn
- **Lenguaje:** Python 3.9+

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura

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
│  • Lógica de negocio completa                                   │
│  • Gestión de entidades (JPA/Hibernate)                         │
│  • Autenticación y autorización                                 │
│  • Sesiones de usuario                                          │
│  • Base de datos relacional                                     │
│  • Orquestación de servicios                                    │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/REST (Cliente interno)
                               │ Llamadas a endpoints de IA
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              MICROSERVICIO IA - Python FastAPI                  │
│                   (utec-planificador-ai)                        │
│                   (Puerto 8000)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐      │
│  │              API LAYER (Controllers)                  │      │
│  ├───────────────────────────────────────────────────────┤      │
│  │  • chatbot_controller.py                              │      │
│  │    - POST /agent/chat/message                         │      │
│  │    - DELETE /agent/chat/session/{id}                  │      │
│  │                                                       │      │
│  │  • suggestion_controller.py                           │      │
│  │    - POST /agent/suggestions                          │      │
│  │                                                       │      │
│  │  • report_controller.py                               │      │
│  │    - POST /agent/report/generate                      │      │
│  └───────────────────────────────────────────────────────┘      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────┐      │
│  │           SERVICE LAYER (Business Logic)              │      │
│  ├───────────────────────────────────────────────────────┤      │
│  │  • chatbot_service.py                                 │      │
│  │  • suggestion_service.py                              │      │
│  │  • report_service.py                                  │      │
│  └───────────────────────────────────────────────────────┘      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────┐      │
│  │              GRAPH LAYER (AI Agent)                   │      │
│  ├───────────────────────────────────────────────────────┤      │
│  │  • chatbot_graph.py (ReactAgentWrapper)               │      │
│  │    - Validación de relevancia educativa               │      │
│  │    - Gestión de contexto y historial                  │      │
│  │    - Routing de herramientas                          │      │
│  │                                                       │      │
│  │  • Tools:                                             │      │
│  │    - pedagogical_help_tool.py                         │      │
│  │    - planificacion_analysis_tool.py                   │      │
│  └───────────────────────────────────────────────────────┘      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────┐      │
│  │          STORAGE LAYER (Session Management)           │      │
│  ├───────────────────────────────────────────────────────┤      │
│  │  • utils.py                                           │      │
│  │    - InMemoryHistory (por sesión)                     │      │
│  │    - Limpieza automática (Thread Daemon)              │      │
│  │    - Timeout: 20 minutos de inactividad               │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                 │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   OPENAI API          │
                    │   (GPT-4o-mini)       │
                    └───────────────────────┘
```

### Flujo de Datos

#### 1. Chatbot Conversacional
```
Usuario interactúa con Frontend
    ↓
Frontend → Backend Java (planificador-utec-be)
    ↓
Backend Java valida sesión, permisos, etc.
    ↓
Backend Java → POST /agent/chat/message (Microservicio IA)
    ↓
chatbot_controller.py (valida request)
    ↓
chatbot_service.py (crea ChatState)
    ↓
ReactAgentWrapper.invoke()
    ↓
┌──────────────────────────────────┐
│ Validación de Relevancia         │
│ (_validate_educational_relevance)│
│                                  │
│ ¿Es relevante educativamente?    │
│  - Consulta pedagógica: SÍ       │
│  - Relacionado con planning: SÍ  │
│  - Tema no relacionado: NO       │
└──────────────────────────────────┘
    ↓
    NO → Mensaje de rechazo
    ↓
    SÍ → Continuar
    ↓
Recuperar historial (get_or_create_history)
    ↓
Routing de herramientas (si aplica)
    ↓
Llamada a OpenAI GPT-4o-mini
    ↓
Guardar en historial
    ↓
Retornar respuesta al microservicio IA
    ↓
Backend Java recibe respuesta
    ↓
Backend Java procesa/enriquece datos
    ↓
Backend Java → Frontend → Usuario
```

#### 2. Generación de Sugerencias
```
Usuario solicita sugerencias en Frontend
    ↓
Frontend → Backend Java
    ↓
Backend Java prepara datos y llama al microservicio
    ↓
Backend Java → POST /agent/suggestions (Microservicio IA)
    ↓
suggestion_controller.py
    ↓
suggestion_service.py
    ↓
Análisis completo de la planificación:
  - Procesos cognitivos
  - Competencias transversales
  - Estrategias de enseñanza
  - Recursos de aprendizaje
  - Vinculación con ODS
  - Principios UDL
    ↓
Llamada a GPT-4o-mini con JSON mode
    ↓
Retornar análisis + sugerencias al Backend Java
    ↓
Backend Java almacena/procesa resultados
    ↓
Backend Java → Frontend → Usuario
```

#### 3. Generación de Reportes
```
Usuario solicita reporte en Frontend
    ↓
Frontend → Backend Java
    ↓
Backend Java recopila estadísticas y planificación desde BD
    ↓
Backend Java → POST /agent/report/generate (Microservicio IA)
    ↓
report_controller.py
    ↓
report_service.py
    ↓
Análisis de estadísticas + planificación:
  - Distribución de procesos cognitivos
  - Balance de modalidades
  - Diversidad de estrategias
  - Evaluación de recursos
  - Alineación con ODS
    ↓
Llamada a GPT-4o-mini con JSON mode
    ↓
Retornar reporte completo al Backend Java con:
  - Rating general (⭐)
  - Análisis detallado
  - Fortalezas
  - Áreas de mejora
  - Recomendaciones accionables
    ↓
Backend Java puede almacenar el reporte en BD
    ↓
Backend Java → Frontend → Usuario
```

---

## 🔗 Integración con Backend Principal

### Responsabilidades del Backend Java (planificador-utec-be)

El backend principal Java Spring Boot es responsable de:

1. **Gestión de Usuario y Autenticación**
   - Autenticación JWT
   - Autorización basada en roles
   - Gestión de sesiones de usuario
   - Control de acceso a recursos

2. **Lógica de Negocio**
   - CRUD de planificaciones docentes
   - Validaciones de negocio
   - Cálculo de estadísticas
   - Gestión de cursos, docentes, programas académicos

3. **Persistencia de Datos**
   - JPA/Hibernate
   - Base de datos relacional (PostgreSQL/MySQL)
   - Entidades: User, CoursePlanning, Activity, Week, etc.
   - Transacciones y consistencia de datos

4. **Orquestación de Servicios**
   - Decide cuándo llamar al microservicio de IA
   - Prepara los datos en formato correcto
   - Consume endpoints REST del microservicio
   - Procesa y enriquece las respuestas de IA
   - Almacena resultados de análisis en BD

### Responsabilidades del Microservicio IA (utec-planificador-ai)

Este microservicio se enfoca exclusivamente en:

1. **Análisis Pedagógico con IA**
   - Procesamiento de lenguaje natural
   - Generación de respuestas conversacionales
   - Análisis de planificaciones con criterios pedagógicos

2. **Gestión de Contexto Conversacional**
   - Historial de chat en memoria (temporal)
   - Limpieza automática de sesiones inactivas
   - NO persiste datos en base de datos

3. **Integración con OpenAI**
   - Llamadas a GPT-4o-mini
   - Gestión de prompts especializados
   - Validación de relevancia educativa

### Flujo de Integración Típico

```
┌──────────┐     ┌─────────────────┐     ┌──────────────┐     ┌──────────┐
│ Frontend │────▶│ Backend Java    │────▶│ Microservicio│────▶│ OpenAI   │
│          │     │ (Spring Boot)   │     │ IA (FastAPI) │     │ API      │
└──────────┘     └─────────────────┘     └──────────────┘     └──────────┘
     ▲                  │                        │                   │
     │                  │                        │                   │
     │                  ▼                        ▼                   ▼
     │           ┌─────────────┐         ┌────────────┐      ┌──────────┐
     │           │ Base de     │         │ Historial  │      │ GPT-4o   │
     └───────────│ Datos       │         │ en Memoria │      │ mini     │
                 │ (PostgreSQL)│         │ (Temporal) │      └──────────┘
                 └─────────────┘         └────────────┘
```

### Ejemplo de Integración: Generar Sugerencias

**Backend Java (planificador-utec-be):**

```java
@Service
public class PlanningAnalysisService {
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Value("${ai.service.url}")
    private String aiServiceUrl; // http://localhost:8000
    
    public SuggestionResponse generateSuggestions(Long planningId) {
        // 1. Recuperar planificación desde BD
        CoursePlanning planning = planningRepository.findById(planningId)
            .orElseThrow(() -> new NotFoundException("Planning not found"));
        
        // 2. Convertir entidad a DTO para el microservicio
        CoursePlanningDTO dto = mapper.toDTO(planning);
        
        // 3. Preparar request para microservicio IA
        SuggestionRequest request = new SuggestionRequest();
        request.setCoursePlanning(dto);
        
        // 4. Llamar al microservicio de IA
        String url = aiServiceUrl + "/agent/suggestions";
        SuggestionResponse response = restTemplate.postForObject(
            url, 
            request, 
            SuggestionResponse.class
        );
        
        // 5. Guardar resultados en BD (opcional)
        AnalysisResult result = new AnalysisResult();
        result.setPlanningId(planningId);
        result.setAnalysis(response.getAnalysis());
        result.setSuggestions(response.getPedagogicalSuggestions());
        result.setCreatedAt(LocalDateTime.now());
        analysisRepository.save(result);
        
        // 6. Retornar al frontend
        return response;
    }
}
```

### Consideraciones de Seguridad

- **El microservicio IA NO implementa autenticación** (es un servicio interno)
- **El backend Java valida** que el usuario tenga permisos antes de llamar al microservicio
- **Recomendación para producción:** Desplegar ambos servicios en red privada o usar API Gateway con autenticación interna

---

## 🔧 Infraestructura y Componentes

### Estructura de Directorios

```
utec-planificador-ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app principal
│   ├── config.py                  # Configuración (OPENAI_KEY)
│   │
│   ├── api/                       # Capa de Controllers (REST)
│   │   ├── __init__.py
│   │   ├── chatbot_controller.py
│   │   ├── suggestion_controller.py
│   │   ├── report_controller.py
│   │   │
│   │   └── schemas/               # DTOs y validación Pydantic
│   │       ├── chat_dto.py
│   │       ├── planification_dto.py
│   │       ├── suggestion_dto.py
│   │       └── report_dto.py
│   │
│   ├── service/                   # Capa de Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── chatbot_service.py
│   │   ├── suggestion_service.py
│   │   └── report_service.py
│   │
│   ├── graph/                     # Capa de Agente IA
│   │   ├── __init__.py
│   │   ├── chatbot_graph.py       # ReactAgentWrapper (núcleo)
│   │   ├── utils.py               # Gestión de sesiones
│   │   │
│   │   ├── schema/
│   │   │   └── chat_state.py      # Estado del chat
│   │   │
│   │   └── tool/                  # Herramientas del agente
│   │       ├── pedagogical_help_tool.py
│   │       └── planificacion_analysis_tool.py
│   │
│   └── utils/                     # Utilidades
│       ├── __init__.py
│       └── enum_descriptions.py   # Descripciones de enumeraciones
│
├── main.py                        # Script de prueba
├── pyproject.toml                 # Dependencias del proyecto
└── .env                           # Variables de entorno (OPENAI_KEY)

```

### Componentes Clave

#### 1. **ReactAgentWrapper** (`chatbot_graph.py`)

El núcleo del sistema de IA. Responsabilidades:

- **Validación de seguridad:** Filtra consultas no educativas
- **Gestión de contexto:** Maneja historial conversacional y planificación
- **Routing inteligente:** Decide cuándo usar herramientas especializadas
- **Integración con OpenAI:** Llamadas al modelo GPT-4o-mini

```python
class ReactAgentWrapper:
    def _validate_educational_relevance(self, user_input, planning_context)
    def _call_openai(self, messages, model="gpt-4o-mini")
    def invoke(self, state: ChatState)
```

#### 2. **Sistema de Sesiones** (`utils.py`)

Gestión eficiente de memoria:

- **InMemoryHistory:** Almacena mensajes por sesión
- **Limpieza automática:** Thread daemon que elimina sesiones inactivas
- **Configuración:**
  - Timeout: 20 minutos de inactividad
  - Limpieza cada: 5 minutos

```python
SESSION_TIMEOUT_MINUTES = 20
CLEANUP_INTERVAL_SECONDS = 300

def get_or_create_history(session_id: str) -> InMemoryHistory
def cleanup_expired_sessions()
def background_cleanup_task()  # Thread daemon
```

#### 3. **Validación de Datos** (`schemas/`)

Uso extensivo de Pydantic para validación:

- **Enums estrictos:** Shift, CognitiveProcess, TeachingStrategy, etc.
- **Validación automática:** FastAPI + Pydantic
- **Type safety:** Tipado fuerte en toda la aplicación

---

## 🌐 Endpoints de la API

### Base URL

```
http://localhost:8000
```

### Documentación Interactiva

```
http://localhost:8000/docs     # Swagger UI
http://localhost:8000/redoc    # ReDoc
```

### ⚠️ Importante: Consumo de Endpoints

**Estos endpoints están diseñados para ser consumidos por el backend Java (planificador-utec-be), NO directamente por el frontend.**

El backend Java:
- Valida permisos y sesiones
- Prepara los datos desde la base de datos
- Llama a estos endpoints
- Procesa y almacena las respuestas
- Retorna los resultados al frontend

Para pruebas y desarrollo, pueden usarse directamente con herramientas como cURL, Postman o los ejemplos de PowerShell provistos.

---

### 1. 💬 Chatbot Pedagógico

#### **POST** `/agent/chat/message`

Interactúa con el chatbot pedagógico para consultas sobre enseñanza, metodologías y mejores prácticas.

**Características:**
- ✅ Mantiene historial conversacional por sesión
- ✅ Acepta contexto de planificación opcional
- ✅ Valida relevancia educativa automáticamente
- ✅ Soporta consultas sobre el tema de la planificación cargada

**Request Body:**

```json
{
  "session_id": "profesor_001",
  "message": "¿Cómo implemento el Aprendizaje Basado en Problemas en mi curso?",
  "coursePlanning": null  // Opcional
}
```

**Con Planificación (Ejemplo):**

```json
{
  "session_id": "profesor_002",
  "message": "¿Qué opinas de mi planificación? ¿Tiene buena distribución de procesos cognitivos?",
  "coursePlanning": {
    "id": 1,
    "shift": "MORNING",
    "description": "Curso de introducción a la programación orientada a objetos",
    "curricularUnit": {
      "name": "Programación I",
      "credits": 4
    },
    "weeklyPlannings": [
      {
        "weekNumber": 1,
        "programmaticContents": [
          {
            "content": "Introducción a POO",
            "activities": [
              {
                "description": "Clase teórica sobre clases y objetos",
                "durationInMinutes": 90,
                "cognitiveProcesses": ["REMEMBER", "UNDERSTAND"],
                "teachingStrategies": ["LECTURE"],
                "learningModality": "IN_PERSON"
              }
            ]
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
  "reply": "Tu planificación muestra una buena base. En cuanto a procesos cognitivos, la semana 1 enfoca principalmente en REMEMBER y UNDERSTAND, lo cual es apropiado para una introducción. Sin embargo, te recomiendo incorporar actividades de niveles superiores (APPLY, ANALYZE, CREATE) en las siguientes semanas..."
}
```

**Códigos de Estado:**
- `200`: Respuesta exitosa
- `400`: Parámetros inválidos (session_id o message vacíos)
- `500`: Error interno del servidor

---

#### **DELETE** `/agent/chat/session/{session_id}`

Elimina una sesión específica y su historial.

**URL Parameter:**
- `session_id`: ID de la sesión a eliminar

**Response:**

```json
{
  "message": "Session 'profesor_001' cleared successfully"
}
```

---

### 2. 📝 Sugerencias de Planificación

#### **POST** `/agent/suggestions`

Analiza una planificación completa y genera sugerencias pedagógicas basadas en mejores prácticas educativas.

**Características:**
- 🎯 Análisis profundo de estructura pedagógica
- 🎯 Evaluación de balance entre modalidades
- 🎯 Análisis de procesos cognitivos (Taxonomía de Bloom)
- 🎯 Evaluación de alineación con ODS
- 🎯 Revisión de principios UDL

**Request Body:**

```json
{
  "coursePlanning": {
    "id": 1,
    "shift": "MORNING",
    "description": "Curso de introducción a la programación",
    "startDate": "2024-03-01",
    "endDate": "2024-07-15",
    "partialGradingSystem": "PGS_1",
    "hoursPerDeliveryFormat": {
      "IN_PERSON": 40,
      "VIRTUAL": 20,
      "HYBRID": 10
    },
    "isRelatedToInvestigation": true,
    "involvesActivitiesWithProductiveSector": false,
    "sustainableDevelopmentGoals": ["SDG_4", "SDG_8", "SDG_9"],
    "universalDesignLearningPrinciples": [
      "MEANS_OF_REPRESENTATION",
      "MEANS_OF_ACTION_EXPRESSION",
      "MEANS_OF_ENGAGEMENT"
    ],
    "curricularUnit": {
      "id": 1,
      "name": "Programación I",
      "credits": 4,
      "domainAreas": ["SOFTWARE_ENGINEERING"],
      "professionalCompetencies": ["SOFTWARE_DESIGN"]
    },
    "weeklyPlannings": [
      // Array de semanas con contenidos y actividades
    ]
  }
}
```

**Response:**

```json
{
  "analysis": "📊 **Análisis de la Planificación del Curso**\n\n✅ **Fortalezas identificadas:**\n- Buena distribución de horas (40 presenciales, 20 virtuales, 10 híbridas)\n- Vinculación con ODS 4, 8 y 9\n- Aplicación de los 3 principios UDL\n\n⚠️ **Áreas de oportunidad:**\n- Solo 15% de actividades en niveles cognitivos superiores (ANALYZE, EVALUATE, CREATE)\n- Alta concentración en LECTURE (45% de las estrategias)\n- Recursos digitales limitados",
  "pedagogicalSuggestions": "1. 🎯 Incrementar actividades de análisis y creación al 30-40% del total\n2. 💡 Diversificar estrategias: incorporar más CASE_STUDY, PROJECTS y FLIPPED_CLASSROOM\n3. 🌐 Añadir recursos digitales interactivos (simuladores, plataformas colaborativas)\n4. 🔬 Diseñar al menos 2 actividades vinculadas con el sector productivo\n5. 📊 Implementar rúbricas detalladas para actividades de creación\n6. 🤝 Fortalecer trabajo colaborativo en modalidad virtual"
}
```

**Códigos de Estado:**
- `200`: Análisis exitoso
- `400`: Planificación no proporcionada o inválida
- `500`: Error en el análisis

---

### 3. 📊 Generación de Reportes

#### **POST** `/agent/report/generate`

Genera un reporte completo de calidad educativa basado en estadísticas del curso y la planificación completa.

**Características:**
- ⭐ Calificación general (EXCELLENT a NEEDS IMPROVEMENT)
- 📈 Score numérico (0-100)
- 📊 Análisis detallado por criterio
- 💪 Identificación de fortalezas
- 🎯 Áreas de mejora
- 💡 Recomendaciones específicas y accionables

**Request Body:**

```json
{
  "courseId": "PROG101-2024",
  "statistics": {
    "cognitiveProcesses": {
      "REMEMBER": 15,
      "UNDERSTAND": 25,
      "APPLY": 30,
      "ANALYZE": 15,
      "EVALUATE": 10,
      "CREATE": 5
    },
    "transversalCompetencies": {
      "COMMUNICATION": 20,
      "TEAMWORK": 25,
      "LEARNING_SELF_REGULATION": 30,
      "CRITICAL_THINKING": 25
    },
    "learningModalities": {
      "IN_PERSON": 50,
      "VIRTUAL": 10,
      "SIMULTANEOUS_IN_PERSON_VIRTUAL": 10,
      "AUTONOMOUS": 30
    },
    "teachingStrategies": {
      "LECTURE": 30,
      "PRACTICAL_ACTIVITY": 25,
      "LABORATORY_PRACTICES": 20,
      "TESTS": 15,
      "CASE_STUDY": 10
    },
    "mostUsedResources": [
      "WHITEBOARD",
      "BOOK_DOCUMENT",
      "ONLINE_EVALUATION",
      "WEBPAGE"
    ],
    "linkedSDGs": {
      "SDG_4": 60,
      "SDG_8": 20,
      "SDG_9": 20
    },
    "averageActivityDurationInMinutes": 65,
    "totalWeeks": 12,
    "totalInPersonHours": 40,
    "totalVirtualHours": 20,
    "totalHybridHours": 10
  },
  "coursePlanning": {
    // Planificación completa (mismo formato que /suggestions)
  }
}
```

**Response:**

```json
{
  "success": true,
  "overallRating": "VERY GOOD ⭐⭐⭐⭐",
  "report": {
    "courseId": "PROG101-2024",
    "analysisDate": "2025-11-26",
    "overallRating": "VERY GOOD ⭐⭐⭐⭐",
    "score": "85%",
    "numericScore": 85,
    "message": "El curso presenta una estructura sólida con buen balance pedagógico",
    "executiveSummary": {
      "totalWeeks": 12,
      "totalHours": 70,
      "inPersonHours": 40,
      "virtualHours": 20,
      "hybridHours": 10,
      "averageActivityDuration": "65 min",
      "totalActivitiesAnalyzed": 100
    },
    "detailedAnalysis": {
      "cognitiveProcesses": "Excelente distribución con 30% en niveles superiores (ANALYZE, EVALUATE, CREATE), favoreciendo el pensamiento crítico...",
      "transversalCompetencies": "Buena diversidad con balance equilibrado entre las 4 principales competencias...",
      "modalityBalance": "Balance adecuado entre presencial (50%) y formatos alternativos...",
      "teachingStrategies": "Variedad metodológica destacable con 5 estrategias diferentes...",
      "resources": "Diversidad apropiada de recursos tradicionales y digitales...",
      "sdgLinkage": "Fuerte alineamiento con ODS 4 (Educación de calidad - 60%)"
    },
    "strengths": [
      "Excelente balance en procesos cognitivos con 30% en niveles superiores",
      "Uso diversificado de estrategias de enseñanza (5 diferentes)",
      "Fuerte vinculación con ODS 4 (Educación de calidad)",
      "Buen balance de competencias transversales"
    ],
    "improvementAreas": [
      "Aumentar actividades de nivel CREATE (actualmente 5%)",
      "Fortalecer la vinculación con el sector productivo",
      "Incrementar recursos digitales interactivos"
    ]
  },
  "recommendations": [
    "📊 Incluir más actividades de evaluación entre pares",
    "🔬 Diseñar al menos una actividad práctica vinculada con empresas",
    "📚 Incorporar casos de estudio reales de la industria",
    "🎯 Añadir rúbricas detalladas para actividades de creación",
    "💻 Integrar herramientas colaborativas online",
    "🌐 Considerar un proyecto final que aborde un ODS específico"
  ]
}
```

**Criterios de Evaluación:**

1. **Procesos Cognitivos** (Taxonomía de Bloom)
   - ✅ Óptimo: 30-40% en niveles superiores
   - ⚠️ Problema: >60% en niveles básicos

2. **Competencias Transversales**
   - ✅ Óptimo: 3+ competencias, distribución equilibrada
   - ⚠️ Problema: <3 competencias o desbalance >3:1

3. **Modalidades de Aprendizaje**
   - ✅ Óptimo: Mezcla según naturaleza del curso
   - ⚠️ Problema: >80% en una sola modalidad

4. **Estrategias de Enseñanza**
   - ✅ Óptimo: 3+ estrategias, LECTURE <50%
   - ⚠️ Problema: <3 estrategias o LECTURE >50%

5. **Duración de Actividades**
   - ✅ Óptimo: 30-90 minutos promedio
   - ⚠️ Problema: <30 o >120 minutos

6. **Recursos de Aprendizaje**
   - ✅ Óptimo: 3+ tipos diferentes
   - ⚠️ Problema: <3 tipos

7. **Vinculación con ODS**
   - ✅ Óptimo: Al menos 1 ODS con alineación clara
   - ⚠️ Problema: Sin vinculación o superficial

**Códigos de Estado:**
- `200`: Reporte generado exitosamente
- `400`: Estadísticas o planificación faltantes
- `500`: Error en la generación

---

## 🔒 Sistema de Seguridad

### Validación de Relevancia Educativa

El chatbot implementa un **sistema de validación multicapa** para garantizar que solo responda a consultas relacionadas con educación y pedagogía.

#### Flujo de Validación

```
Usuario envía prompt
    ↓
Extraer contexto de planificación (si existe)
    ↓
Enviar prompt + contexto al validador LLM (GPT-4o-mini)
    ↓
┌─────────────────────────────────────┐
│  Validador analiza:                 │
│  1. ¿Es consulta pedagógica?        │
│  2. ¿Está relacionada con planning? │
│  3. ¿Es meta-consulta válida?       │
│  4. ¿Es saludo/cortesía?            │
└─────────────────────────────────────┘
    ↓
¿Es válido?
    │
    ├─ NO → Mensaje de rechazo
    │        "Lo siento, solo puedo ayudarte con temas
    │         relacionados a pedagogía y educación..."
    │
    └─ SÍ → Procesar normalmente
```

#### Reglas de Aceptación

**✅ CONSULTAS ACEPTADAS:**

1. **Consultas pedagógicas generales:**
   - "¿Cómo enseñar matemáticas a niños de primaria?"
   - "¿Qué estrategias usar para evaluar competencias?"
   - "Dame ejemplos de rúbricas analíticas"
   - "¿Cómo implementar el aula invertida?"

2. **Consultas sobre planificación docente:**
   - "Ayúdame a diseñar objetivos de aprendizaje"
   - "¿Cómo integrar los ODS en mi planificación?"
   - "¿Qué actividades recomiendas para nivel ANALYZE?"

3. **Consultas relacionadas al contexto de la planificación:**
   - Con planificación de **Gastronomía**: "Dame una receta de milanesa" ✅
   - Con planificación de **Química**: "Explica la tabla periódica" ✅
   - Con planificación de **Educación Física**: "Reglas del básquetbol" ✅

4. **Meta-consultas sobre la conversación:**
   - "¿Cuál fue mi último mensaje?"
   - "Repite eso por favor"
   - "Explícame mejor"
   - "Hola", "Gracias", "OK"

**❌ CONSULTAS RECHAZADAS:**

1. **Temas no educativos sin contexto:**
   - "Dame una receta de milanesa" (sin planificación de cocina) ❌
   - "¿Quién ganó el mundial?" ❌
   - "Cuéntame un chiste" ❌

2. **Temas no relacionados a la planificación:**
   - Con planificación de **Matemáticas**: "Dame una receta de pizza" ❌
   - Con planificación de **Historia**: "¿Cómo jugar ajedrez?" ❌

#### Implementación Técnica

**Validador LLM:**
```python
def _validate_educational_relevance(self, user_input: str, planning_context: dict):
    """
    Valida si el prompt es relevante al contexto educativo/pedagógico.
    Retorna (is_valid: bool, reason: str)
    """
    # Construir contexto de planificación
    context_info = extract_planning_context(planning_context)
    
    # Llamar a GPT-4o-mini con temperatura baja (0.3)
    validation_prompt = """
    Eres un filtro de seguridad para un asistente pedagógico.
    
    Contexto de planificación: {context_info}
    Consulta del usuario: "{user_input}"
    
    REGLAS:
    1. Consultas pedagógicas: SIEMPRE VÁLIDAS
    2. Relacionadas con planning: VÁLIDAS
    3. Meta-consultas: VÁLIDAS
    4. Contenido sin contexto educativo: INVÁLIDAS
    
    Responde:
    VÁLIDO: [SÍ o NO]
    RAZÓN: [explicación breve]
    """
    
    response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": validation_prompt}],
        temperature=0.3,
        max_tokens=150
    )
    
    # Parsear respuesta
    return parse_validation_response(response)
```

#### Política Fail-Safe

Si el validador falla (error de API, timeout):
- **Política:** Fail-open (permitir por defecto)
- **Log:** Warning registrado
- **Razón:** Preferir falsos positivos a denegar servicios legítimos

#### Logs de Ejemplo

**Consulta Rechazada:**
```
WARNING - Prompt rechazado por no ser relevante: 'Dame una receta de milanesa'
          Razón: No hay contexto educativo
```

**Consulta Aceptada:**
```
INFO - Prompt aceptado: 'Dame una receta de milanesa'
       Razón: Relacionado con la planificación de Gastronomía Argentina
```

---

## ⏱️ Gestión de Sesiones

### Sistema de Limpieza Automática

El sistema implementa un **mecanismo dual de limpieza** para prevenir fugas de memoria:

#### Arquitectura de Sesiones

```
┌─────────────────────────────────────────────────────┐
│        session_memory_store (Diccionario)           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  session_id_1: (InMemoryHistory, timestamp)         │
│  session_id_2: (InMemoryHistory, timestamp)         │
│  session_id_3: (InMemoryHistory, timestamp)         │
│  ...                                                │
│                                                     │
└─────────────────────────────────────────────────────┘
           ▲                          ▲
           │                          │
    ┌──────┴────────┐         ┌───────┴────────┐
    │   Limpieza    │         │    Limpieza    │
    │  Sincrónica   │         │   Asíncrona    │
    │  (Inmediata)  │         │  (Background)  │
    └───────────────┘         └────────────────┘
```

#### 1. Limpieza Sincrónica (Inmediata)

Se ejecuta en cada acceso a una sesión:

```python
def get_or_create_history(session_id: str) -> InMemoryHistory:
    current_time = datetime.now()
    
    # Limpieza inmediata de sesiones expiradas
    cleanup_expired_sessions()
    
    # Crear o recuperar sesión
    if session_id not in session_memory_store:
        session_memory_store[session_id] = (InMemoryHistory(), current_time)
        logger.info(f"Nueva sesión creada: {session_id}")
    else:
        # Actualizar timestamp
        history, _ = session_memory_store[session_id]
        session_memory_store[session_id] = (history, current_time)
    
    return session_memory_store[session_id][0]
```

#### 2. Limpieza Asíncrona (Background Thread)

Thread daemon que corre continuamente:

```python
def background_cleanup_task():
    """Tarea en segundo plano que limpia sesiones expiradas periódicamente"""
    while True:
        try:
            time.sleep(CLEANUP_INTERVAL_SECONDS)  # 300 segundos = 5 min
            cleanup_expired_sessions()
        except Exception as e:
            logger.error(f"Error en limpieza automática: {e}")

# Thread daemon - se cierra automáticamente con la aplicación
cleanup_thread = threading.Thread(target=background_cleanup_task, daemon=True)
cleanup_thread.start()
```

#### Función de Limpieza

```python
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
```

#### Configuración

```python
SESSION_TIMEOUT_MINUTES = 20      # Timeout de inactividad
CLEANUP_INTERVAL_SECONDS = 300    # Frecuencia de limpieza (5 min)
```

#### Escenario de Uso

**Sin limpieza automática (Problema):**
```
Usuario A → envía mensaje → sesión creada en RAM
Usuario A → nunca vuelve → sesión permanece en RAM indefinidamente
100 usuarios inactivos → fuga de memoria progresiva
```

**Con limpieza automática (Solución):**
```
Usuario A → envía mensaje → sesión creada (timestamp: T0)
Usuario A → no envía nada por 20 minutos
Thread limpieza → detecta inactividad (T0 + 20min < T_ahora)
Thread limpieza → elimina sesión
Memoria → liberada automáticamente
```

#### Logs de Ejemplo

```
2025-11-26 14:24:08 - app.graph.utils - INFO - Nueva sesión creada: profesor_123
2025-11-26 14:44:10 - app.graph.utils - INFO - Sesión expirada eliminada: profesor_123
2025-11-26 14:44:10 - app.graph.utils - INFO - Limpieza completada: 1 sesión(es) eliminada(s)
```

#### Seguridad Thread-Safe

- **Thread daemon:** Se cierra limpiamente con la aplicación
- **Operaciones atómicas:** Diccionarios en CPython son thread-safe para operaciones básicas
- **Manejo de excepciones:** El thread continúa ejecutándose incluso si ocurre un error

---

## 📦 Modelos de Datos

### Enumeraciones Principales

#### CognitiveProcess (Taxonomía de Bloom Revisada)

```python
class CognitiveProcessEnum(str, Enum):
    REMEMBER = "REMEMBER"          # Recordar
    UNDERSTAND = "UNDERSTAND"      # Comprender
    APPLY = "APPLY"                # Aplicar
    ANALYZE = "ANALYZE"            # Analizar
    EVALUATE = "EVALUATE"          # Evaluar
    CREATE = "CREATE"              # Crear
    NOT_DETERMINED = "NOT_DETERMINED"
```

**Descripción pedagógica:**
- **REMEMBER:** Recuperar conocimiento de memoria
- **UNDERSTAND:** Construir significado del material
- **APPLY:** Usar información en situaciones nuevas
- **ANALYZE:** Descomponer y determinar relaciones
- **EVALUATE:** Juicios basados en criterios
- **CREATE:** Formar algo nuevo y coherente

#### TransversalCompetency

```python
class TransversalCompetencyEnum(str, Enum):
    COMMUNICATION = "COMMUNICATION"
    TEAMWORK = "TEAMWORK"
    LEARNING_SELF_REGULATION = "LEARNING_SELF_REGULATION"
    CRITICAL_THINKING = "CRITICAL_THINKING"
    NOT_DETERMINED = "NOT_DETERMINED"
```

#### TeachingStrategy

```python
class TeachingStrategyEnum(str, Enum):
    LECTURE = "LECTURE"                    # Clase magistral
    DEBATE = "DEBATE"                      # Debate
    TEAMWORK = "TEAMWORK"                  # Trabajo en equipo
    FIELD_ACTIVITY = "FIELD_ACTIVITY"      # Actividad de campo
    PRACTICAL_ACTIVITY = "PRACTICAL_ACTIVITY"
    LABORATORY_PRACTICES = "LABORATORY_PRACTICES"
    TESTS = "TESTS"
    RESEARCH_ACTIVITIES = "RESEARCH_ACTIVITIES"
    FLIPPED_CLASSROOM = "FLIPPED_CLASSROOM"
    DISCUSSION = "DISCUSSION"
    SMALL_GROUP_TUTORIALS = "SMALL_GROUP_TUTORIALS"
    PROJECTS = "PROJECTS"
    CASE_STUDY = "CASE_STUDY"
    OTHER = "OTHER"
    NOT_DETERMINED = "NOT_DETERMINED"
```

#### SustainableDevelopmentGoal (ODS)

```python
class SustainableDevelopmentGoalEnum(str, Enum):
    SDG_1 = "SDG_1"    # Fin de la pobreza
    SDG_2 = "SDG_2"    # Hambre cero
    SDG_3 = "SDG_3"    # Salud y bienestar
    SDG_4 = "SDG_4"    # Educación de calidad ⭐
    SDG_5 = "SDG_5"    # Igualdad de género
    SDG_6 = "SDG_6"    # Agua limpia
    SDG_7 = "SDG_7"    # Energía asequible
    SDG_8 = "SDG_8"    # Trabajo decente ⭐
    SDG_9 = "SDG_9"    # Innovación ⭐
    SDG_10 = "SDG_10"  # Reducción de desigualdades
    SDG_11 = "SDG_11"  # Ciudades sostenibles
    SDG_12 = "SDG_12"  # Consumo responsable
    SDG_13 = "SDG_13"  # Acción por el clima
    SDG_14 = "SDG_14"  # Vida submarina
    SDG_15 = "SDG_15"  # Vida terrestre
    SDG_16 = "SDG_16"  # Paz y justicia
    SDG_17 = "SDG_17"  # Alianzas
```

#### UniversalDesignLearningPrinciple (DUA)

```python
class UniversalDesignLearningPrincipleEnum(str, Enum):
    MEANS_OF_ENGAGEMENT = "MEANS_OF_ENGAGEMENT"
    MEANS_OF_REPRESENTATION = "MEANS_OF_REPRESENTATION"
    MEANS_OF_ACTION_EXPRESSION = "MEANS_OF_ACTION_EXPRESSION"
    NONE = "NONE"
```

### DTOs Principales

#### CoursePlanningDTO

```python
class CoursePlanningDTO(BaseModel):
    id: Optional[int]
    shift: ShiftEnum
    description: str
    startDate: str
    endDate: str
    partialGradingSystem: PartialGradingSystemEnum
    hoursPerDeliveryFormat: Dict[str, int]
    isRelatedToInvestigation: bool
    involvesActivitiesWithProductiveSector: bool
    sustainableDevelopmentGoals: List[SustainableDevelopmentGoalEnum]
    universalDesignLearningPrinciples: List[UniversalDesignLearningPrincipleEnum]
    curricularUnit: Optional[CurricularUnitDTO]
    weeklyPlannings: List[WeeklyPlanningDTO]
```

#### ActivityDTO

```python
class ActivityDTO(BaseModel):
    id: Optional[int]
    description: str
    durationInMinutes: int
    cognitiveProcesses: List[CognitiveProcessEnum]
    transversalCompetencies: List[TransversalCompetencyEnum]
    learningModality: LearningModalityEnum
    teachingStrategies: List[TeachingStrategyEnum]
    learningResources: List[LearningResourceEnum]
```

#### ChatState

```python
@dataclass
class ChatState:
    session_id: str
    input: str
    history: List[Dict[str, Any]]
    planning: Optional[Dict[str, Any]]
```

---

## ⚙️ Configuración e Instalación

### Requisitos Previos

- **Python:** 3.9 o superior
- **OpenAI API Key:** Cuenta activa con créditos
- **Sistema Operativo:** Windows, Linux o macOS

### Instalación

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-org/utec-planificador-ai.git
cd utec-planificador-ai
```

#### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

O usando pyproject.toml:

```bash
pip install -e .
```

**Dependencias principales:**
- fastapi>=0.104.0
- uvicorn>=0.24.0
- openai>=1.0.0
- python-dotenv>=1.0.0
- pydantic>=2.0.0

#### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
OPENAI_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ IMPORTANTE:** Nunca commitear el archivo `.env` al repositorio.

### Ejecutar el Servidor

#### Modo Desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Modo Producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Verificar Instalación

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy"
}
```

**Swing:**
```
http://localhost:8000/docs
```

### Integración con Backend Java

Para que el backend Java (planificador-utec-be) pueda consumir este microservicio, configurar en su `application.properties` o `application.yml`:

```yaml
# application.yml
ai:
  service:
    url: http://localhost:8000
    timeout: 30000  # 30 segundos
```

O para ambientes productivos con Docker:

```yaml
ai:
  service:
    url: http://utec-planificador-ai:8000
```

### Configuración Avanzada

#### Ajustar Timeouts de Sesión

Editar `app/graph/utils.py`:

```python
SESSION_TIMEOUT_MINUTES = 30       # Cambiar de 20 a 30 minutos
CLEANUP_INTERVAL_SECONDS = 600     # Cambiar de 5 a 10 minutos
```

#### Configurar Modelo GPT

Editar `app/graph/chatbot_graph.py`:

```python
def _call_openai(self, messages: list, model: str = "gpt-4o"):  # Cambiar modelo
    # ...
```

#### Logging

Configuración en `app/main.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Cambiar nivel de logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')  # Agregar archivo de log
    ]
)
```

---

## 💡 Casos de Uso

### Caso 1: Consulta Pedagógica General

**Escenario:** Un docente quiere aprender sobre una metodología.

**Flujo completo del sistema:**

```
1. Docente escribe en el chat del Frontend: 
   "¿Cómo implemento el Aprendizaje Basado en Proyectos en mi curso de ingeniería?"

2. Frontend envía request al Backend Java

3. Backend Java:
   - Valida sesión y permisos del usuario
   - Obtiene el session_id del docente
   - Prepara el request para el microservicio IA

4. Backend Java → Microservicio IA (POST /agent/chat/message)

5. Microservicio IA:
   - Validador verifica que es consulta pedagógica → ✅ VÁLIDA
   - Sistema recupera historial de la sesión
   - Construye contexto con historial previo
   - Llama a GPT-4o-mini con el prompt
   - Guarda respuesta en historial
   - Retorna respuesta al Backend Java

6. Backend Java recibe la respuesta y la retorna al Frontend

7. Frontend muestra la respuesta al docente
```

**Request directo al microservicio (solo para pruebas):**
```bash
curl -X POST "http://localhost:8000/agent/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "prof_001",
    "message": "¿Cómo implemento el Aprendizaje Basado en Proyectos en mi curso de ingeniería?"
  }'
```

**Beneficio:** El docente recibe asesoramiento pedagógico experto sin necesidad de buscar en múltiples fuentes, mientras el backend Java mantiene control sobre la autenticación y el contexto del usuario.

---

### Caso 2: Análisis de Planificación Existente

**Escenario:** Un docente tiene una planificación y quiere retroalimentación.

**Flujo completo del sistema:**

```
1. Docente solicita análisis desde el Frontend

2. Frontend → Backend Java (solicitud de análisis)

3. Backend Java:
   - Valida permisos del usuario sobre esa planificación
   - Recupera la planificación completa desde BD (entidades JPA)
   - Convierte las entidades a DTOs
   - Prepara request para el microservicio IA

4. Backend Java → Microservicio IA (POST /agent/suggestions)

5. Microservicio IA:
   - Recibe planificación completa
   - Extrae métricas clave:
     • Distribución de procesos cognitivos
     • Estrategias de enseñanza utilizadas
     • Recursos de aprendizaje
     • Vinculación con ODS
   - Envía a GPT-4o-mini para análisis profundo
   - Recibe análisis estructurado + sugerencias
   - Retorna al Backend Java

6. Backend Java:
   - Opcionalmente almacena el análisis en BD
   - Registra la acción en logs/auditoría
   - Retorna al Frontend

7. Frontend muestra el análisis al docente
```

**Request directo al microservicio (solo para pruebas):**
```bash
curl -X POST "http://localhost:8000/agent/suggestions" \
  -H "Content-Type: application/json" \
  -d @planificacion.json
```

**Resultado:** El docente obtiene:
- Análisis objetivo de su planificación
- Identificación de fortalezas y debilidades
- 5-8 sugerencias concretas y accionables
- El análisis queda registrado en el sistema principal para futuras referencias

---

### Caso 3: Generación de Reporte de Calidad

**Escenario:** Coordinador académico necesita evaluar la calidad de un curso.

**Flujo completo del sistema:**

```
1. Coordinador solicita reporte desde el Frontend

2. Frontend → Backend Java (solicitud de reporte)

3. Backend Java:
   - Valida permisos del coordinador
   - Recupera la planificación completa desde BD
   - Calcula estadísticas del curso:
     • Distribución de procesos cognitivos
     • Balance de modalidades
     • Frecuencia de estrategias
     • Recursos utilizados
   - Prepara request con estadísticas + planificación

4. Backend Java → Microservicio IA (POST /agent/report/generate)

5. Microservicio IA:
   - Recibe estadísticas + planificación
   - Analiza contra criterios pedagógicos:
     • Balance cognitivo
     • Diversidad metodológica
     • Alineación con ODS
     • Aplicación de UDL
   - GPT-4o-mini genera reporte estructurado
   - Sistema calcula rating general
   - Retorna reporte completo al Backend Java

6. Backend Java:
   - Almacena el reporte en BD con timestamp
   - Vincula el reporte al curso y coordinador
   - Genera PDF (opcional)
   - Retorna al Frontend

7. Frontend muestra el reporte al coordinador
```

**Request directo al microservicio (solo para pruebas):**
```bash
curl -X POST "http://localhost:8000/agent/report/generate" \
  -H "Content-Type: application/json" \
  -d @report_request.json
```

**Resultado:** El coordinador obtiene:
- Rating de calidad (⭐⭐⭐⭐)
- Score numérico (85/100)
- Análisis detallado por criterio
- Fortalezas identificadas
- Áreas de mejora priorizadas
- Recomendaciones específicas
- Historial de reportes previos del curso (almacenado en BD por el backend Java)

---

### Caso 4: Chat Contextual con Planificación

**Escenario:** Docente quiere consejos específicos sobre su planificación de Gastronomía.

**Request:**
```bash
curl -X POST "http://localhost:8000/agent/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "prof_gastronomia",
    "message": "Dame ideas de recetas para enseñar técnicas de emplatado",
    "coursePlanning": {
      "curricularUnit": {"name": "Gastronomía Avanzada"},
      "description": "Curso de técnicas culinarias profesionales"
    }
  }'
```

**Flujo:**
1. Validador detecta contexto de Gastronomía
2. Pregunta sobre recetas es VÁLIDA (relacionada con el curso)
3. Sistema incorpora contexto de planificación
4. GPT-4o-mini responde con recetas + enfoque pedagógico
5. Respuesta es educativa y relevante al curso

**Beneficio:** El sistema entiende el contexto académico y proporciona contenido relevante para la enseñanza.

---

### Caso 5: Conversación Continua con Memoria

**Escenario:** Docente mantiene una conversación extendida sobre su curso.

**Secuencia:**

**Mensaje 1:**
```json
{
  "session_id": "prof_123",
  "message": "Quiero mejorar mi curso de programación"
}
```

**Respuesta 1:** "Para ayudarte mejor, ¿podrías compartir qué aspectos específicos te preocupan? Por ejemplo: evaluación, metodología, recursos..."

**Mensaje 2:**
```json
{
  "session_id": "prof_123",
  "message": "Principalmente la evaluación, creo que dependo demasiado de exámenes"
}
```

**Respuesta 2:** "Entiendo tu preocupación sobre la evaluación. Te sugiero diversificar con: 1) Proyectos prácticos (30%), 2) Code reviews entre pares (20%), 3) Portafolio de código (20%), 4) Exámenes conceptuales (30%)..."

**Mensaje 3:**
```json
{
  "session_id": "prof_123",
  "message": "¿Cómo implemento el code review entre pares?"
}
```

**Flujo:**
1. Sistema recupera historial de `prof_123`
2. Contexto: Curso de programación + preocupación por evaluación
3. GPT-4o-mini responde con guía específica de code review
4. Respuesta es coherente con la conversación previa

**Beneficio:** Experiencia conversacional natural con memoria de contexto.

---

## 📊 Costos y Performance

### Costos Estimados (GPT-4o-mini)

| Operación              | Tokens Aprox. | Costo por Llamada | Llamadas con $5 USD |
|------------------------|---------------|-------------------|---------------------|
| Chat simple            | 300-500       | ~$0.0005-0.001    | ~5,000-10,000       |
| Chat con planificación | 800-1,200     | ~$0.001-0.002     | ~2,500-5,000        |
| Sugerencias            | 1,500-2,000   | ~$0.003-0.005     | ~1,000-1,600        |
| Reporte                | 2,000-2,500   | ~$0.004-0.006     | ~800-1,250          |

**Total estimado:** Con $5 USD puedes realizar aproximadamente:
- 5,000 consultas de chat simples
- 1,000 análisis de planificación completos
- 800 reportes detallados

### Performance

**Tiempos de Respuesta Promedio:**
- Chat simple: 1-2 segundos
- Chat con planificación: 2-3 segundos
- Sugerencias: 3-5 segundos
- Reportes: 4-6 segundos

**Capacidad:**
- Sesiones concurrentes: Limitado por memoria RAM
- Limpieza automática: Mantiene memoria estable
- Escalabilidad: Horizontal (múltiples workers Uvicorn)

---

## 🚀 Próximos Pasos y Mejoras

### Corto Plazo

- [ ] Implementar autenticación interna entre servicios (API Key o mTLS)
- [ ] Agregar rate limiting a nivel de microservicio
- [ ] Métricas y monitoreo (Prometheus)
- [ ] Tests unitarios y de integración

### Mediano Plazo

- [ ] Persistencia de sesiones (Redis)
- [ ] Soporte para múltiples idiomas
- [ ] Dashboard de analíticas
- [ ] Integración con bases de datos institucionales

### Largo Plazo

- [ ] Fine-tuning de modelo específico para UTEC
- [ ] Sistema de recomendaciones proactivas
- [ ] Análisis predictivo de calidad
- [ ] Integración con LMS (Moodle, Canvas)

---

**Última actualización:** 26 de Noviembre, 2025  
**Versión:** 1.0.0

