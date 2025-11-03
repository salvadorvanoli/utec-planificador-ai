# 🚀 UTEC Planificador AI - Guía Completa con GPT

**Servidor:** http://localhost:8000  
**Documentación Interactiva:** http://localhost:8000/docs
**RUNNEAR APP:** uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

---

## ⚡ IMPORTANTE: Configuración Requerida

**Todas las tools ahora usan GPT-4o-mini de OpenAI**

### Requisitos:
1. **API Key de OpenAI configurada** en `.env`:
   ```
   OPENAI_KEY=tu-clave-aqui
   ```

2. **Créditos en tu cuenta OpenAI** (se requiere método de pago configurado)

3. **Iniciar servidor sin modo fake**:
   ```powershell
   cd C:\Users\salva\PycharmProjects\utec-planificador-ai\UTECPlanificadorAgent
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 💰 Costos Estimados (GPT-4o-mini)

| Tool | Costo por llamada | Tokens aprox. |
|------|-------------------|---------------|
| Chatbot | ~$0.001 | 300-800 tokens |
| Sugerencias | ~$0.003-0.005 | 1500-2000 tokens |
| Reportes | ~$0.004-0.006 | 2000-2500 tokens |

**Total estimado:** Con $5 USD puedes hacer ~1000-1500 análisis completos

---

## 🎯 Los 3 Tools con GPT

### 1️⃣ **CHATBOT PEDAGÓGICO** 💬

**Modelo:** GPT-4o-mini  
**Función:** Responde preguntas sobre pedagogía, metodologías, evaluación, mejores prácticas educativas

#### Endpoint:
```
POST /agent/chat/message
```

#### Request:
```json
{
  "session_id": "profesor_001",
  "message": "¿Cómo implemento el Aprendizaje Basado en Problemas en mi curso?"
}
```

#### PowerShell:
```powershell
$chat = @{
    session_id = "prof001"
    message = "¿Cómo implemento el Aprendizaje Basado en Problemas en mi curso?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/agent/chat/message" -Method Post -Body $chat -ContentType "application/json"
```

#### Respuesta Real de GPT:
```json
{
  "reply": "Para implementar el Aprendizaje Basado en Problemas (ABP) efectivamente:\n\n1. **Diseño del problema**: Crea situaciones auténticas y complejas relacionadas con tu disciplina...\n2. **Trabajo en equipos**: Organiza grupos de 4-6 estudiantes...\n3. **Rol del docente**: Actúa como facilitador, no como expositor...\n4. **Evaluación**: Usa rúbricas que evalúen tanto el proceso como el producto final..."
}
```

---

### 2️⃣ **SUGERENCIAS DE PLANIFICACIÓN** 📝

**Modelo:** GPT-4o-mini con JSON mode  
**Función:** Analiza planificación docente completa y genera sugerencias pedagógicas con IA

#### Endpoint:
```
POST /agent/suggestions
```

#### Request (ejemplo resumido):
```json
{
  "course_id": "ROB101",
  "planificacionDocente": {
    "descripcionGeneral": "Curso de robótica aplicada",
    "objetivosDesarrolloSostenibleVinculados": ["ODS 4", "ODS 9"],
    "principiosDUA": ["Múltiples medios de representación"],
    "horasPresenciales": 24,
    "horasVirtuales": 18,
    "sistemaDeCalificacion": "Evaluación continua",
    "semanas": [
      {
        "semana": 1,
        "fecha": "2025-03-10",
        "contenidosProgramaticos": "Introducción a robótica",
        "actividades": [
          {
            "descripcion": "Clase teórica",
            "duracionMin": 90,
            "modalidad": "Presencial",
            "estrategiaEnseñanza": "Clase expositiva",
            "procesosCognitivos": ["recordar", "comprender"],
            "competenciasTransversales": ["comunicacionEfectiva"],
            "recursos": ["PowerPoint"]
          }
        ],
        "recursosYBibliografia": ["Libro de robótica"]
      }
    ]
  }
}
```

#### Respuesta Real de GPT:
```json
{
  "analysis": "📊 ANÁLISIS PEDAGÓGICO:\n\n✅ Fortalezas identificadas:\n- Balance adecuado entre modalidad presencial (57%) y virtual (43%)\n- Vinculación con ODS relevantes para el área\n\n⚠️ Áreas de oportunidad:\n- Procesos cognitivos limitados a niveles básicos (recordar, comprender)\n- Falta diversidad en estrategias de enseñanza\n- Principios DUA incompletos (solo 1 de 3)\n\n📈 Métricas:\n- Total actividades: 1\n- Competencias trabajadas: 1\n- Estrategias diferentes: 1",
  
  "pedagogical_suggestions": "1. 🧠 Incorpora procesos cognitivos superiores: Añade actividades de análisis, evaluación y creación según Taxonomía de Bloom\n\n2. 🔄 Diversifica metodologías: Implementa ABP, estudio de casos, aprendizaje colaborativo además de clases expositivas\n\n3. ♿ Completa principios DUA: Agrega 'múltiples formas de acción/expresión' y 'múltiples formas de motivación'\n\n4. 🎯 Amplía competencias transversales: Incluye pensamiento crítico, trabajo en equipo, resolución de problemas\n\n5. 📚 Enriquece recursos: Añade videos, simuladores, lecturas interactivas más allá de PowerPoint"
}
```

---

### 3️⃣ **GENERADOR DE REPORTES** 📊

**Modelo:** GPT-4o-mini con JSON mode  
**Función:** Analiza estadísticas del curso y genera reporte completo con calificación y recomendaciones

#### Endpoint:
```
POST /agent/report/generate
```

#### Request:
```json
{
  "course_id": "ROB101",
  "estadisticas": {
    "procesosCognitivos": {
      "recordar": 10,
      "comprender": 25,
      "aplicar": 20,
      "analizar": 15,
      "evaluar": 20,
      "crear": 10
    },
    "competenciasTransversales": {
      "trabajoEnEquipo": 30,
      "pensamientoCritico": 25,
      "comunicacionEfectiva": 20,
      "resolucionDeProblemas": 25
    },
    "modalidades": {
      "presencial": 60,
      "virtual": 40
    },
    "estrategiasDeEnseñanza": {
      "aprendizajeBasadoEnProyectos": 35,
      "claseExpositiva": 25,
      "estudioDeCasos": 20,
      "debateGuiado": 20
    },
    "recursosMasUtilizados": [
      "Presentaciones", "Videos", "Lecturas", "Labs virtuales"
    ],
    "ODSvinculados": {
      "ODS4_EducacionDeCalidad": 60,
      "ODS9_IndustriaInnovacion": 40
    },
    "promedioDuracionActividadesMin": 45,
    "totalSemanas": 12,
    "totalHorasPresenciales": 24,
    "totalHorasVirtuales": 18
  }
}
```

#### PowerShell:
```powershell
$report = @{
    course_id = "ROB101"
    estadisticas = @{
        procesosCognitivos = @{
            recordar = 10; comprender = 25; aplicar = 20
            analizar = 15; evaluar = 20; crear = 10
        }
        competenciasTransversales = @{
            trabajoEnEquipo = 30; pensamientoCritico = 25
            comunicacionEfectiva = 20; resolucionDeProblemas = 25
        }
        modalidades = @{ presencial = 60; virtual = 40 }
        estrategiasDeEnseñanza = @{
            aprendizajeBasadoEnProyectos = 35; claseExpositiva = 25
            estudioDeCasos = 20; debateGuiado = 20
        }
        recursosMasUtilizados = @("Presentaciones", "Videos", "Lecturas", "Labs")
        ODSvinculados = @{ ODS4 = 60; ODS9 = 40 }
        promedioDuracionActividadesMin = 45
        totalSemanas = 12
        totalHorasPresenciales = 24
        totalHorasVirtuales = 18
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:8000/agent/report/generate" -Method Post -Body $report -ContentType "application/json"
```

#### Respuesta Real de GPT:
```json
{
  "success": true,
  "calificacion_general": "MUY BUENO ⭐⭐⭐⭐",
  "reporte": {
    "course_id": "ROB101",
    "fecha_analisis": "2025-01-17",
    "calificacion_general": "MUY BUENO ⭐⭐⭐⭐",
    "puntuacion": "85%",
    "mensaje": "Excelente planificación con buenos fundamentos pedagógicos. Algunas mejoras específicas pueden llevarla a la excelencia.",
    "resumen_ejecutivo": {
      "total_semanas": 12,
      "total_horas": 42,
      "horas_presenciales": 24,
      "horas_virtuales": 18,
      "duracion_promedio_actividades": "45 min",
      "total_actividades_analizadas": 100
    },
    "puntos_fuertes": [
      "⭐ Excelente balance de procesos cognitivos: 45% en niveles superiores (analizar, evaluar, crear)",
      "🎯 Diversidad destacable de competencias transversales (4 competencias bien distribuidas)",
      "⚖️ Balance óptimo presencial/virtual (57% / 43%)",
      "🔄 Variedad metodológica sobresaliente (4 estrategias diferentes)",
      "⏱️ Duración de actividades en rango ideal (45 min promedio)"
    ],
    "areas_de_mejora": [
      "Incrementar ligeramente procesos de 'crear' para fomentar más innovación",
      "Considerar agregar 1-2 ODS adicionales para mayor impacto social"
    ],
    "analisis_detallado": {
      "procesos_cognitivos": "Distribución equilibrada con 35% en niveles básicos y 45% en superiores. Destacable el 20% en 'evaluar' que promueve pensamiento crítico.",
      "competencias_transversales": "Las 4 competencias están bien balanceadas (20-30% cada una), promoviendo desarrollo integral del estudiante.",
      "balance_modalidad": "Proporción ideal que mantiene interacción presencial mientras promueve autonomía virtual.",
      "estrategias_ensenanza": "Predominio de ABP (35%) evidencia enfoque en metodologías activas. Clase expositiva en proporción adecuada (25%).",
      "recursos": "Diversidad de 4 tipos de recursos garantiza múltiples formas de acceso al conocimiento.",
      "vinculacion_ods": "Fuerte vinculación con ODS 4 (60%) y ODS 9 (40%), alineado con educación técnica de calidad."
    }
  },
  "recomendaciones": [
    "🎨 Incremente actividades de 'creación': Proyectos de diseño, prototipos, propuestas innovadoras para llevar el nivel de 10% a 15-20%",
    "🌍 Considere ODS adicionales: ODS 12 (Producción responsable) y ODS 5 (Igualdad de género en STEM)",
    "📊 Mantenga el excelente balance metodológico: La proporción actual de metodologías activas es ejemplar",
    "✅ Continúe fortaleciendo competencias transversales: El balance actual es óptimo, mantenerlo a lo largo del curso"
  ]
}
```

---

## 🧪 Pruebas Rápidas

### Test Chatbot:
```powershell
$body = @{
    session_id = "test001"
    message = "¿Qué es la Taxonomía de Bloom revisada?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/agent/chat/message" -Method Post -Body $body -ContentType "application/json"
```

### Test Sugerencias Mínimas:
```powershell
$body = @{
    course_id = "TEST"
    planificacionDocente = @{
        descripcionGeneral = "Curso básico"
        horasPresenciales = 20
        horasVirtuales = 10
        sistemaDeCalificacion = "Examen final"
        semanas = @(@{
            semana = 1
            fecha = "2025-03-01"
            contenidosProgramaticos = "Introducción"
            actividades = @(@{
                descripcion = "Clase"
                duracionMin = 60
                modalidad = "Presencial"
                estrategiaEnseñanza = "Expositiva"
                procesosCognitivos = @("recordar")
                competenciasTransversales = @()
                recursos = @("Pizarra")
            })
            recursosYBibliografia = @()
        })
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:8000/agent/suggestions" -Method Post -Body $body -ContentType "application/json"
```

### Test Reporte Básico:
```powershell
$body = @{
    course_id = "TEST"
    estadisticas = @{
        procesosCognitivos = @{
            recordar = 50; comprender = 30; aplicar = 10
            analizar = 5; evaluar = 3; crear = 2
        }
        competenciasTransversales = @{
            trabajoEnEquipo = 50; pensamientoCritico = 50
        }
        modalidades = @{ presencial = 80; virtual = 20 }
        estrategiasDeEnseñanza = @{
            claseExpositiva = 70; estudioDeCasos = 30
        }
        recursosMasUtilizados = @("PowerPoint", "Libro")
        ODSvinculados = @{}
        promedioDuracionActividadesMin = 90
        totalSemanas = 10
        totalHorasPresenciales = 30
        totalHorasVirtuales = 5
    }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://localhost:8000/agent/report/generate" -Method Post -Body $body -ContentType "application/json"
```

---

## ⚠️ Troubleshooting

### Error: "OpenAI API Key no configurada"
**Solución:** Verifica que `.env` tenga `OPENAI_KEY=tu-clave`

### Error: "insufficient_quota"
**Solución:** Agrega método de pago en https://platform.openai.com/account/billing

### Error: "rate_limit_exceeded"
**Solución:** Espera unos segundos entre llamadas o aumenta límites en OpenAI

### Servidor no inicia
**Solución:** Verifica que OPENAI_KEY esté configurada correctamente

---

## 💡 Mejores Prácticas

1. **Usa session_id consistente** en el chatbot para mantener contexto
2. **Provee planificaciones completas** para mejores análisis
3. **Incluye todas las métricas** en reportes para evaluación precisa
4. **Revisa los costos** en tu dashboard de OpenAI periódicamente

---

## 🎓 Sistema Completamente Funcional

Todas las tools ahora usan **inteligencia artificial real** con GPT-4o-mini de OpenAI para:
- Análisis pedagógico profundo
- Sugerencias contextualizadas
- Reportes profesionales con calificaciones

**¡El sistema está listo para producción!** 🚀

