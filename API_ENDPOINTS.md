# 📋 API Endpoints Documentation - UTEC Planificador AI Agent

## Base URL
```
http://localhost:8000
```

---

## 🔥 Cambios Recientes

### Actualizaciones Importantes:
1. **Chat Endpoint** - Ahora acepta **opcionalmente** una planificación de curso
2. **Report Endpoint** - Ahora **requiere obligatoriamente** tanto las estadísticas como la planificación completa
3. **Suggestions Endpoint** - Sin cambios (siempre requiere planificación)

---

## 🤖 1. Chatbot - Pedagogical Queries

### **POST** `/agent/chat/message`
Query the chatbot about pedagogical practices. Optionally include a course planning for context-specific advice.

#### Request Body (Sin planificación):
```json
{
  "session_id": "profesor_001",
  "message": "¿Cómo implemento el Aprendizaje Basado en Problemas en mi curso?"
}
```

#### Request Body (Con planificación - OPCIONAL):
```json
{
  "session_id": "profesor_001",
  "message": "¿Qué opinas de mi planificación? ¿Tiene buena distribución de procesos cognitivos?",
  "coursePlanning": {
    "id": 1,
    "shift": "MORNING",
    "description": "Curso de introducción a la programación orientada a objetos",
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
      "domainAreas": ["SOFTWARE_ENGINEERING", "PROGRAMMING"],
      "professionalCompetencies": ["SOFTWARE_DESIGN", "PROBLEM_SOLVING"],
      "term": {
        "id": 1,
        "number": 1,
        "program": {
          "id": 1,
          "name": "Ingeniería en Computación",
          "durationInTerms": 8,
          "totalCredits": 240
        }
      }
    },
    "weeklyPlannings": [
      {
        "id": 1,
        "weekNumber": 1,
        "startDate": "2024-03-01",
        "bibliographicReferences": [
          "Deitel, P. & Deitel, H. (2020). Java How to Program. 11th Edition. Pearson."
        ],
        "programmaticContents": [
          {
            "id": 1,
            "content": "Introducción a la programación orientada a objetos",
            "activities": [
              {
                "id": 1,
                "description": "Explicación teórica de conceptos básicos de POO",
                "durationInMinutes": 90,
                "cognitiveProcesses": ["REMEMBER", "UNDERSTAND"],
                "transversalCompetencies": ["CRITICAL_THINKING", "COMMUNICATION"],
                "learningModality": "IN_PERSON",
                "teachingStrategies": ["LECTURE"],
                "learningResources": ["EXHIBITION", "WHITEBOARD"]
              }
            ]
          }
        ],
        "activities": []
      }
    ]
  }
}
```

#### Response:
```json
{
  "reply": "Tu planificación muestra una buena base. En cuanto a procesos cognitivos, la semana 1 enfoca principalmente en REMEMBER y UNDERSTAND, lo cual es apropiado para una introducción. Sin embargo, te recomiendo incorporar actividades de niveles superiores (APPLY, ANALYZE, CREATE) en las siguientes semanas para desarrollar el pensamiento crítico..."
}
```

---

### **DELETE** `/agent/chat/session/{session_id}`
Delete a specific chat session.

#### URL Parameter:
- `session_id`: Session ID to delete

#### Response:
```json
{
  "message": "Session 'profesor_001' cleared successfully"
}
```

---

## 📝 2. Course Planning Suggestions

### **POST** `/agent/suggestions`
Analyzes a complete course planning and provides improvement suggestions based on pedagogical best practices.

**⚠️ Nota:** Este endpoint **siempre requiere** una planificación completa.

#### Request Body:
```json
{
  "coursePlanning": {
    "id": 1,
    "shift": "MORNING",
    "description": "Curso de introducción a la programación orientada a objetos",
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
      "domainAreas": ["SOFTWARE_ENGINEERING", "PROGRAMMING"],
      "professionalCompetencies": ["SOFTWARE_DESIGN", "PROBLEM_SOLVING"],
      "term": {
        "id": 1,
        "number": 1,
        "program": {
          "id": 1,
          "name": "Ingeniería en Computación",
          "durationInTerms": 8,
          "totalCredits": 240
        }
      }
    },
    "weeklyPlannings": [
      {
        "id": 1,
        "weekNumber": 1,
        "startDate": "2024-03-01",
        "bibliographicReferences": [
          "Deitel, P. & Deitel, H. (2020). Java How to Program. 11th Edition. Pearson.",
          "Sierra, K. & Bates, B. (2005). Head First Java. O'Reilly Media."
        ],
        "programmaticContents": [
          {
            "id": 1,
            "content": "Introducción a la programación orientada a objetos",
            "activities": [
              {
                "id": 1,
                "description": "Explicación teórica de conceptos básicos de POO: clases, objetos, métodos",
                "durationInMinutes": 90,
                "cognitiveProcesses": ["REMEMBER", "UNDERSTAND"],
                "transversalCompetencies": ["CRITICAL_THINKING", "COMMUNICATION"],
                "learningModality": "IN_PERSON",
                "teachingStrategies": ["LECTURE"],
                "learningResources": ["WHITEBOARD", "BOOK_DOCUMENT"]
              },
              {
                "id": 2,
                "description": "Ejercicio práctico: crear primera clase en Java",
                "durationInMinutes": 60,
                "cognitiveProcesses": ["APPLY", "CREATE"],
                "transversalCompetencies": ["LEARNING_SELF_REGULATION"],
                "learningModality": "IN_PERSON",
                "teachingStrategies": ["PRACTICAL_ACTIVITY"],
                "learningResources": ["BOOK_DOCUMENT"]
              }
            ]
          }
        ],
        "activities": []
      }
    ]
  }
}
```

#### Response:
```json
{
  "analysis": "📊 **Análisis de la Planificación del Curso**\n\n✅ La planificación presenta una estructura básica sólida con enfoque práctico desde la primera semana...",
  "pedagogicalSuggestions": "1. Incrementar actividades de nivel CREATE (actualmente bajo)\n2. Incluir más recursos digitales interactivos\n3. Diversificar estrategias de enseñanza más allá de LECTURE\n4. Fortalecer la vinculación con el sector productivo"
}
```

---

## 📊 3. Course Report Generation

### **POST** `/agent/report/generate`
Generates a complete report analyzing course quality based on both statistics and the complete planning.

**⚠️ Nota:** Este endpoint ahora **requiere obligatoriamente** tanto las estadísticas como la planificación completa.

#### Request Body:
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
    "id": 1,
    "shift": "MORNING",
    "description": "Curso de introducción a la programación orientada a objetos",
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
      "MEANS_OF_ACTION_EXPRESSION"
    ],
    "curricularUnit": {
      "id": 1,
      "name": "Programación I",
      "credits": 4,
      "domainAreas": ["SOFTWARE_ENGINEERING"],
      "professionalCompetencies": ["SOFTWARE_DESIGN"],
      "term": {
        "id": 1,
        "number": 1,
        "program": {
          "id": 1,
          "name": "Ingeniería en Computación",
          "durationInTerms": 8,
          "totalCredits": 240
        }
      }
    },
    "weeklyPlannings": [
      {
        "id": 1,
        "weekNumber": 1,
        "startDate": "2024-03-01",
        "bibliographicReferences": ["Deitel, P. & Deitel, H. (2020). Java How to Program."],
        "programmaticContents": [
          {
            "id": 1,
            "content": "Introducción a POO",
            "activities": [
              {
                "id": 1,
                "description": "Clase teórica",
                "durationInMinutes": 90,
                "cognitiveProcesses": ["REMEMBER", "UNDERSTAND"],
                "transversalCompetencies": ["CRITICAL_THINKING"],
                "learningModality": "IN_PERSON",
                "teachingStrategies": ["LECTURE"],
                "learningResources": ["WHITEBOARD"]
              }
            ]
          }
        ],
        "activities": []
      }
    ]
  }
}
```

#### Response:
```json
{
  "success": true,
  "report": {
    "courseId": "PROG101-2024",
    "analysisDate": "2025-11-03",
    "overallRating": "VERY GOOD ⭐⭐⭐⭐",
    "score": "85%",
    "message": "El curso presenta una estructura sólida con buen balance pedagógico y alineamiento con los ODS",
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
      "cognitiveProcesses": "Excelente distribución con 30% en niveles superiores (ANALYZE, EVALUATE, CREATE), lo cual favorece el pensamiento crítico y la innovación...",
      "transversalCompetencies": "Buena diversidad de competencias transversales con balance equilibrado entre las 4 principales...",
      "modalityBalance": "Balance adecuado entre presencial (50%) y formatos alternativos, favoreciendo la flexibilidad...",
      "teachingStrategies": "Variedad metodológica destacable con 5 estrategias diferentes, aunque LECTURE sigue siendo predominante...",
      "resources": "Diversidad apropiada de recursos tradicionales y digitales...",
      "sdgLinkage": "Fuerte alineamiento con ODS 4 (Educación de calidad - 60%), complementado con ODS 8 y 9 relacionados con innovación y desarrollo profesional"
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
    "📊 Incluir más actividades de evaluación entre pares para fortalecer el aprendizaje colaborativo",
    "🔬 Diseñar al menos una actividad práctica vinculada con empresas del sector tecnológico",
    "📚 Incorporar casos de estudio reales de la industria del software",
    "🎯 Añadir rúbricas detalladas para las actividades de creación",
    "💻 Integrar herramientas colaborativas online para trabajo en equipo",
    "🌐 Considerar implementar un proyecto final que aborde un ODS específico"
  ],
  "overallRating": "VERY GOOD ⭐⭐⭐⭐"
}
```

---

## 🔑 Enumerations Reference

### Shift
- `MORNING` - Turno mañana
- `EVENING` - Turno tarde/noche

### PartialGradingSystem
- `PGS_1` a `PGS_12` - Sistemas de calificación parcial

### SustainableDevelopmentGoals (SDGs)
- `SDG_1`: Fin de la pobreza
- `SDG_2`: Hambre cero
- `SDG_3`: Salud y bienestar
- `SDG_4`: **Educación de calidad**
- `SDG_5`: Igualdad de género
- `SDG_6`: Agua limpia y saneamiento
- `SDG_7`: Energía asequible y no contaminante
- `SDG_8`: **Trabajo decente y crecimiento económico**
- `SDG_9`: **Industria, innovación e infraestructura**
- `SDG_10`: Reducción de las desigualdades
- `SDG_11`: Ciudades y comunidades sostenibles
- `SDG_12`: Producción y consumo responsables
- `SDG_13`: Acción por el clima
- `SDG_14`: Vida submarina
- `SDG_15`: Vida de ecosistemas terrestres
- `SDG_16`: Paz, justicia e instituciones sólidas
- `SDG_17`: Alianzas para lograr los objetivos

### UniversalDesignLearningPrinciples
- `MEANS_OF_ENGAGEMENT` - Múltiples medios de motivación
- `MEANS_OF_REPRESENTATION` - Múltiples medios de representación
- `MEANS_OF_ACTION_EXPRESSION` - Múltiples medios de acción y expresión
- `NONE` - Sin principio específico

### CognitiveProcess
- `REMEMBER` - Recordar (nivel básico)
- `UNDERSTAND` - Comprender (nivel básico)
- `APPLY` - Aplicar (nivel medio)
- `ANALYZE` - Analizar (nivel superior)
- `EVALUATE` - Evaluar (nivel superior)
- `CREATE` - Crear (nivel superior)
- `NOT_DETERMINED` - No determinado

### TransversalCompetency
- `COMMUNICATION` - Comunicación efectiva
- `TEAMWORK` - Trabajo en equipo
- `LEARNING_SELF_REGULATION` - Autorregulación del aprendizaje
- `CRITICAL_THINKING` - Pensamiento crítico
- `NOT_DETERMINED` - No determinado

### LearningModality
- `VIRTUAL` - Virtual/Online
- `IN_PERSON` - Presencial
- `SIMULTANEOUS_IN_PERSON_VIRTUAL` - Híbrido simultáneo
- `AUTONOMOUS` - Autónomo
- `NOT_DETERMINED` - No determinado

### TeachingStrategy
- `LECTURE` - Clase expositiva
- `DEBATE` - Debate
- `TEAMWORK` - Trabajo en equipo
- `FIELD_ACTIVITY` - Actividad de campo
- `PRACTICAL_ACTIVITY` - Actividad práctica
- `LABORATORY_PRACTICES` - Prácticas de laboratorio
- `TESTS` - Pruebas/Evaluaciones
- `RESEARCH_ACTIVITIES` - Actividades de investigación
- `FLIPPED_CLASSROOM` - Aula invertida
- `DISCUSSION` - Discusión
- `SMALL_GROUP_TUTORIALS` - Tutorías en grupos pequeños
- `PROJECTS` - Proyectos
- `CASE_STUDY` - Estudio de casos
- `OTHER` - Otra estrategia
- `NOT_DETERMINED` - No determinado

### LearningResource
- `EXHIBITION` - Exposición/Presentación
- `BOOK_DOCUMENT` - Libro/Documento
- `DEMONSTRATION` - Demostración
- `WHITEBOARD` - Pizarra
- `ONLINE_COLLABORATION_TOOL` - Herramienta de colaboración online
- `ONLINE_LECTURE` - Clase online
- `ONLINE_FORUM` - Foro online
- `ONLINE_EVALUATION` - Evaluación online
- `GAME` - Juego educativo
- `SURVEY` - Encuesta
- `VIDEO` - Video
- `INFOGRAPHIC` - Infografía
- `WEBPAGE` - Página web
- `OTHER` - Otro recurso
- `NOT_DETERMINED` - No determinado

---

## 📝 Important Notes

### Chat Endpoint Updates
- **Planificación opcional**: Si se proporciona una planificación en el request del chat, el asistente tendrá contexto adicional para dar respuestas más específicas y personalizadas sobre esa planificación en particular.
- **Sin planificación**: El chat funciona normalmente respondiendo preguntas generales sobre pedagogía basándose en la documentación disponible.

### Report Endpoint Updates
- **Planificación obligatoria**: Ahora el reporte requiere TANTO las estadísticas como la planificación completa.
- **Análisis más profundo**: Con acceso a la planificación completa, el sistema puede generar análisis más detallados y contextualizados, correlacionando las estadísticas con el contenido real del curso.
- **Recomendaciones específicas**: Las sugerencias serán más precisas al tener visibilidad completa de las actividades, recursos y estrategias utilizadas.

### Suggestions Endpoint
- **Sin cambios**: Mantiene su funcionalidad original, siempre requiriendo una planificación completa para generar sugerencias pedagógicas.

### SDG Integration
- El sistema comprende el significado completo de cada ODS (Objetivo de Desarrollo Sostenible).
- Puede analizar y sugerir cómo integrar mejor los ODS en las planificaciones.
- Evalúa la coherencia entre los ODS declarados y las actividades reales del curso.

---

## 🚀 Quick Start Examples

### 1. Consulta general sin planificación
```bash
curl -X POST http://localhost:8000/agent/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_001",
    "message": "¿Qué es el aprendizaje basado en proyectos?"
  }'
```

### 2. Consulta con contexto de planificación
```bash
curl -X POST http://localhost:8000/agent/chat/message \
  -H "Content-Type: application/json" \
  -d @request_with_planning.json
```

### 3. Generar sugerencias
```bash
curl -X POST http://localhost:8000/agent/suggestions \
  -H "Content-Type: application/json" \
  -d @course_planning.json
```

### 4. Generar reporte completo
```bash
curl -X POST http://localhost:8000/agent/report/generate \
  -H "Content-Type: application/json" \
  -d @report_request.json
```

---

## 📧 Support

For issues or questions, please contact the development team.

