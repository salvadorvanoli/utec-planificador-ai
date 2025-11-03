# 📋 API Endpoints Documentation - UTEC Planificador AI Agent

## Base URL
```
http://localhost:8000
```

---

## 🤖 1. Chatbot - Pedagogical Queries

### **POST** `/agent/chat/message`
Query the chatbot about pedagogical practices using documentation.

#### Request Body:
```json
{
  "session_id": "profesor_001",
  "message": "¿Cómo implemento el Aprendizaje Basado en Problemas en mi curso?"
}
```

#### Response:
```json
{
  "reply": "Basándome en la documentación pedagógica, el Aprendizaje Basado en Problemas..."
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
Analyzes a course planning and provides improvement suggestions.

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
    "sustainableDevelopmentGoals": [
      "SDG_4",
      "SDG_8",
      "SDG_9"
    ],
    "universalDesignLearningPrinciples": [
      "MEANS_OF_REPRESENTATION",
      "MEANS_OF_ACTION_EXPRESSION",
      "MEANS_OF_ENGAGEMENT"
    ],
    "curricularUnit": {
      "id": 1,
      "name": "Programación I",
      "credits": 4,
      "domainAreas": [
        "SOFTWARE_ENGINEERING",
        "PROGRAMMING"
      ],
      "professionalCompetencies": [
        "SOFTWARE_DESIGN",
        "PROBLEM_SOLVING"
      ],
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
                "cognitiveProcesses": [
                  "REMEMBER",
                  "UNDERSTAND"
                ],
                "transversalCompetencies": [
                  "CRITICAL_THINKING",
                  "COMMUNICATION"
                ],
                "learningModality": "IN_PERSON",
                "teachingStrategies": [
                  "LECTURE"
                ],
                "learningResources": [
                  "WHITEBOARD",
                  "BOOK_DOCUMENT"
                ]
              },
              {
                "id": 2,
                "description": "Ejercicio práctico: crear primera clase en Java",
                "durationInMinutes": 60,
                "cognitiveProcesses": [
                  "APPLY",
                  "CREATE"
                ],
                "transversalCompetencies": [
                  "LEARNING_SELF_REGULATION"
                ],
                "learningModality": "IN_PERSON",
                "teachingStrategies": [
                  "PRACTICAL_ACTIVITY"
                ],
                "learningResources": [
                  "BOOK_DOCUMENT"
                ]
              }
            ]
          },
          {
            "id": 2,
            "content": "Sintaxis básica de Java",
            "activities": [
              {
                "id": 3,
                "description": "Demostración de sintaxis: variables, tipos de datos, operadores",
                "durationInMinutes": 45,
                "cognitiveProcesses": [
                  "UNDERSTAND",
                  "REMEMBER"
                ],
                "transversalCompetencies": [
                  "CRITICAL_THINKING"
                ],
                "learningModality": "IN_PERSON",
                "teachingStrategies": [
                  "DEMONSTRATION"
                ],
                "learningResources": [
                  "WHITEBOARD"
                ]
              }
            ]
          }
        ],
        "activities": [
          {
            "id": 4,
            "description": "Quiz de evaluación sobre conceptos introductorios",
            "durationInMinutes": 20,
            "cognitiveProcesses": [
              "REMEMBER",
              "UNDERSTAND"
            ],
            "transversalCompetencies": [
              "LEARNING_SELF_REGULATION"
            ],
            "learningModality": "AUTONOMOUS",
            "teachingStrategies": [
              "TESTS"
            ],
            "learningResources": [
              "ONLINE_EVALUATION"
            ]
          }
        ]
      },
      {
        "id": 2,
        "weekNumber": 2,
        "startDate": "2024-03-08",
        "bibliographicReferences": [
          "Eckel, B. (2006). Thinking in Java. 4th Edition. Prentice Hall.",
          "Bloch, J. (2018). Effective Java. 3rd Edition. Addison-Wesley."
        ],
        "programmaticContents": [
          {
            "id": 3,
            "content": "Estructuras de control: condicionales y bucles",
            "activities": [
              {
                "id": 5,
                "description": "Teoría sobre if-else, switch, for, while",
                "durationInMinutes": 60,
                "cognitiveProcesses": [
                  "UNDERSTAND",
                  "ANALYZE"
                ],
                "transversalCompetencies": [
                  "CRITICAL_THINKING"
                ],
                "learningModality": "IN_PERSON",
                "teachingStrategies": [
                  "LECTURE"
                ],
                "learningResources": [
                  "WHITEBOARD",
                  "BOOK_DOCUMENT"
                ]
              },
              {
                "id": 6,
                "description": "Laboratorio: implementar algoritmos con estructuras de control",
                "durationInMinutes": 90,
                "cognitiveProcesses": [
                  "APPLY",
                  "ANALYZE",
                  "CREATE"
                ],
                "transversalCompetencies": [
                  "LEARNING_SELF_REGULATION",
                  "CRITICAL_THINKING"
                ],
                "learningModality": "IN_PERSON",
                "teachingStrategies": [
                  "LABORATORY_PRACTICES",
                  "PRACTICAL_ACTIVITY"
                ],
                "learningResources": [
                  "BOOK_DOCUMENT"
                ]
              }
            ]
          }
        ],
        "activities": [
          {
            "id": 7,
            "description": "Tarea: resolver conjunto de ejercicios de programación",
            "durationInMinutes": 120,
            "cognitiveProcesses": [
              "APPLY",
              "ANALYZE"
            ],
            "transversalCompetencies": [
              "LEARNING_SELF_REGULATION"
            ],
            "learningModality": "AUTONOMOUS",
            "teachingStrategies": [
              "PRACTICAL_ACTIVITY"
            ],
            "learningResources": [
              "BOOK_DOCUMENT",
              "WEBPAGE"
            ]
          }
        ]
      }
    ]
  }
}
```

#### Response:
```json
{
  "analysis": "📊 **Análisis de la Planificación del Curso**\n\n✅ La planificación presenta...",
  "pedagogicalSuggestions": "1. Incrementar actividades de nivel CREATE...\n2. Incluir más recursos digitales..."
}
```

---

## 📊 3. Course Report Generation

### **POST** `/agent/report/generate`
Generates a complete report on course performance and quality based on statistics.

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
  }
}
```

#### Response:
```json
{
  "success": true,
  "report": {
    "courseId": "PROG101-2024",
    "analysisDate": "2025-01-17",
    "overallRating": "GOOD ⭐⭐⭐",
    "score": "72%",
    "message": "El curso muestra una estructura sólida con oportunidades de mejora",
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
      "cognitiveProcesses": "Balance adecuado con 30% en niveles superiores...",
      "transversalCompetencies": "Buena diversidad de competencias trabajadas...",
      "modalityBalance": "Predominancia presencial con espacio para virtualidad...",
      "teachingStrategies": "Variedad metodológica con 5 estrategias diferentes...",
      "resources": "Recursos tradicionales y digitales balanceados...",
      "sdgLinkage": "Fuerte vinculación con ODS 4 (Educación de Calidad)"
    },
    "strengths": [
      "Excelente balance de competencias transversales",
      "Diversidad de estrategias de enseñanza",
      "Fuerte vinculación con ODS relevantes"
    ],
    "improvementAreas": [
      "Aumentar actividades de nivel CREATE",
      "Incrementar uso de modalidades híbridas",
      "Diversificar recursos digitales"
    ]
  },
  "recommendations": [
    "📈 Aumentar de 5% a 15% las actividades de nivel CREATE para fomentar innovación",
    "💻 Incorporar más recursos digitales interactivos para el aprendizaje virtual",
    "🔄 Implementar al menos 2 actividades en modalidad híbrida por semana",
    "🎯 Incluir más evaluaciones formativas continuas"
  ],
  "overallRating": "GOOD ⭐⭐⭐"
}
```

---

## 🏥 System Endpoints

### **GET** `/`
Basic service information.

#### Response:
```json
{
  "message": "UTEC Planificador AI Agent",
  "status": "online",
  "version": "0.1.0"
}
```

---

### **GET** `/health`
Service health check.

#### Response:
```json
{
  "status": "healthy"
}
```

---

## 📌 Important Notes

### Enums (matching Java Backend)

#### Shift
- `MORNING`
- `EVENING`

#### Delivery Format
- `IN_PERSON`
- `VIRTUAL`
- `HYBRID`

#### Partial Grading System
- `PGS_1` through `PGS_12`

#### Sustainable Development Goals
- `SDG_1` through `SDG_17`

#### Universal Design Learning Principles
- `MEANS_OF_ENGAGEMENT`
- `MEANS_OF_REPRESENTATION`
- `MEANS_OF_ACTION_EXPRESSION`
- `NONE`

#### Cognitive Processes (Bloom's Taxonomy)
- `REMEMBER`
- `UNDERSTAND`
- `APPLY`
- `ANALYZE`
- `EVALUATE`
- `CREATE`
- `NOT_DETERMINED`

#### Transversal Competencies
- `COMMUNICATION`
- `TEAMWORK`
- `LEARNING_SELF_REGULATION`
- `CRITICAL_THINKING`
- `NOT_DETERMINED`

#### Learning Modalities
- `VIRTUAL`
- `IN_PERSON`
- `SIMULTANEOUS_IN_PERSON_VIRTUAL`
- `AUTONOMOUS`
- `NOT_DETERMINED`

#### Teaching Strategies
- `LECTURE`
- `DEBATE`
- `TEAMWORK`
- `FIELD_ACTIVITY`
- `PRACTICAL_ACTIVITY`
- `LABORATORY_PRACTICES`
- `TESTS`
- `RESEARCH_ACTIVITIES`
- `FLIPPED_CLASSROOM`
- `DISCUSSION`
- `SMALL_GROUP_TUTORIALS`
- `PROJECTS`
- `CASE_STUDY`
- `OTHER`
- `NOT_DETERMINED`

#### Learning Resources
- `EXHIBITION`
- `BOOK_DOCUMENT`
- `DEMONSTRATION`
- `WHITEBOARD`
- `ONLINE_COLLABORATION_TOOL`
- `ONLINE_LECTURE`
- `ONLINE_FORUM`
- `ONLINE_EVALUATION`
- `GAME`
- `SURVEY`
- `VIDEO`
- `INFOGRAPHIC`
- `WEBPAGE`
- `OTHER`
- `NOT_DETERMINED`

---

## 🚀 Usage Examples with cURL

### Chatbot
```bash
curl -X POST http://localhost:8000/agent/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "profesor_001",
    "message": "¿Cómo implemento el Aprendizaje Basado en Problemas?"
  }'
```

### Suggestions
```bash
curl -X POST http://localhost:8000/agent/suggestions \
  -H "Content-Type: application/json" \
  -d @course_planning.json
```

### Report
```bash
curl -X POST http://localhost:8000/agent/report/generate \
  -H "Content-Type: application/json" \
  -d @statistics.json
```

---

## ⚙️ Required Environment Variables

Make sure you have configured the `.env` file:

```env
OPENAI_API_KEY=your_key_here
```

- `OPENAI_API_KEY`: Your OpenAI API key

