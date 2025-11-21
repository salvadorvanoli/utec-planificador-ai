# 🔒 Sistema de Seguridad del Chatbot - Validación Educativa

## 📋 Resumen

Se implementó un sistema de validación que asegura que el chatbot **solo responda a consultas relacionadas con pedagogía, enseñanza y educación**, rechazando consultas fuera de este contexto.

## 🎯 Objetivo

Prevenir que el chatbot sea utilizado para propósitos no educativos (recetas, deportes, entretenimiento, etc.) mientras mantiene flexibilidad para consultas educativas legítimas.

## 🔧 Implementación

### Archivo modificado: `app/graph/chatbot_graph.py`

Se agregó el método `_validate_educational_relevance()` que:

1. **Analiza el prompt del usuario** usando un LLM como filtro de seguridad
2. **Considera el contexto de la planificación** si está disponible
3. **Retorna** si el prompt es válido o no, con una razón

### Flujo de validación:

```
Usuario envía prompt
    ↓
Extraer contexto de planificación (si existe)
    ↓
Enviar prompt + contexto al validador LLM
    ↓
¿Es válido? ─── NO → Devolver mensaje de rechazo
    │
   SÍ
    ↓
Procesar prompt normalmente
```

## ✅ Criterios de Aceptación

### Consultas ACEPTADAS:

1. **Consultas pedagógicas generales:**
   - "¿Cómo enseñar matemáticas a niños de primaria?"
   - "¿Qué estrategias usar para evaluar competencias?"
   - "Dame ejemplos de rúbricas analíticas"

2. **Consultas sobre planificación docente:**
   - "Ayúdame a diseñar objetivos de aprendizaje"
   - "¿Cómo integrar los ODS en mi planificación?"

3. **Consultas relacionadas al contexto de la planificación:**
   - Con planificación de **Cocina**: "Dame una receta de milanesa" ✅
   - Con planificación de **Química**: "Explica la tabla periódica" ✅
   - Con planificación de **Deportes**: "Reglas del fútbol" ✅

### Consultas RECHAZADAS:

1. **Temas no educativos sin contexto:**
   - "Dame una receta de milanesa" (sin planificación de cocina) ❌
   - "¿Quién ganó el mundial de fútbol?" ❌
   - "Cuéntame un chiste" ❌

2. **Temas no relacionados a la planificación:**
   - Con planificación de **Matemáticas**: "Dame una receta de pizza" ❌
   - Con planificación de **Historia**: "¿Cómo jugar ajedrez?" ❌

## 📝 Ejemplos de Uso

### Ejemplo 1: Rechazo por falta de contexto

**Entrada:**
```json
{
  "session_id": "user_123",
  "input": "Dame una receta de milanesa napolitana",
  "planning": null
}
```

**Respuesta:**
```
Lo siento, pero solo puedo ayudarte con temas relacionados a pedagogía, 
enseñanza, planificación docente y educación. 

¿En qué puedo asistirte con tu planificación o práctica docente?
```

**Log:**
```
WARNING - Prompt rechazado por no ser relevante: 'Dame una receta de milanesa napolitana' 
          Razón: No hay contexto educativo
```

---

### Ejemplo 2: Aceptación por contexto válido

**Entrada:**
```json
{
  "session_id": "user_456",
  "input": "Dame una receta de milanesa napolitana",
  "planning": {
    "subject": "Gastronomía Argentina",
    "description": "Curso de cocina tradicional para estudiantes de gastronomía"
  }
}
```

**Respuesta:**
```
Claro, aquí está la receta de milanesa napolitana para tu clase de gastronomía...
[respuesta completa del chatbot]
```

**Log:**
```
INFO - Prompt aceptado: 'Dame una receta de milanesa napolitana' 
       Razón: Relacionado con la planificación de Gastronomía
```

---

### Ejemplo 3: Consulta pedagógica (siempre aceptada)

**Entrada:**
```json
{
  "session_id": "user_789",
  "input": "¿Cómo puedo enseñar fracciones a niños de primaria?",
  "planning": null
}
```

**Respuesta:**
```
Aquí hay algunas estrategias efectivas para enseñar fracciones...
[respuesta pedagógica completa]
```

**Log:**
```
INFO - Prompt aceptado: '¿Cómo puedo enseñar fracciones...' 
       Razón: Consulta pedagógica sobre metodología de enseñanza
```

## 🔍 Funcionamiento Técnico

### Validador LLM

El sistema usa `gpt-4o-mini` con temperatura baja (0.3) para clasificar prompts.

#### Extracción de contexto:

El validador extrae información clave de la planificación:
1. **Nombre de la Unidad Curricular**: Busca en `curricularUnit.name`, `name`, o `subject`
2. **Descripción del curso**: Del campo `description`
3. **Contenido programático**: De `weeklyPlannings[0].programmaticContents[0].content`

```python
validation_prompt = """Eres un filtro de seguridad para un asistente pedagógico.

Contexto de planificación disponible:
- Unidad Curricular: Cocina 1
- Descripción del curso: Curso básico de técnicas culinarias...

Consulta del usuario: "Dame una receta de milanesa napolitana"

REGLAS IMPORTANTES:
1. Si hay contexto de planificación Y la consulta está relacionada con ESE tema: ES VÁLIDA
   Ejemplo: Unidad "Cocina 1" + consulta "receta" = VÁLIDA
   
2. Consultas sobre CÓMO ENSEÑAR cualquier tema: SIEMPRE VÁLIDAS
   
3. Consultas sobre contenido SIN contexto relacionado: INVÁLIDAS
   Ejemplo: Planificación "Matemáticas" + "receta" = INVÁLIDA

ANALIZA CUIDADOSAMENTE el nombre de la Unidad Curricular.
"""
```

### Formato de respuesta del validador:

```
VÁLIDO: SÍ
RAZÓN: La consulta está relacionada con el contexto de la planificación de cocina
```

o

```
VÁLIDO: NO
RAZÓN: La consulta sobre recetas no tiene relación con educación sin contexto apropiado
```

## 🛡️ Seguridad y Fail-Safe

### Política Fail-Open

Si el validador falla (error de API, timeout, etc.):
- **Se permite el prompt por defecto**
- Se registra un log de warning
- Evita bloquear usuarios legítimos por problemas técnicos

```python
except Exception as e:
    logger.error(f"Error en validación: {e}")
    return True, "Error en validación, permitiendo por defecto"
```

## 📊 Logs y Monitoreo

### Logs generados:

**Prompt aceptado:**
```
INFO - Validación de relevancia: VÁLIDO: SÍ\nRAZÓN: Consulta pedagógica
INFO - Prompt aceptado: '<texto>' - Razón: Consulta pedagógica
```

**Prompt rechazado:**
```
INFO - Validación de relevancia: VÁLIDO: NO\nRAZÓN: Sin contexto educativo
WARNING - Prompt rechazado por no ser relevante: '<texto>' - Razón: Sin contexto educativo
```

### Métricas útiles a monitorear:

- Tasa de rechazo de prompts
- Tipos de consultas rechazadas (para ajustar filtro)
- Falsos positivos/negativos

### Testing manual con la API:

```bash
# Caso 1: Debe rechazar
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test",
    "message": "Dame una receta de pizza"
  }'

# Caso 2: Debe aceptar
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test",
    "message": "¿Cómo evaluar el trabajo colaborativo?"
  }'
```

## ⚙️ Configuración

### Ajustar sensibilidad del filtro:

Editar `app/graph/chatbot_graph.py`:

```python
# Temperatura del validador (más bajo = más estricto)
temperature=0.3  # Actual: 0.3 (recomendado: 0.2-0.4)

# Tokens máximos de respuesta del validador
max_tokens=150  # Suficiente para la respuesta estructurada
```

### Modificar criterios de validación:

Editar el `validation_prompt` en el método `_validate_educational_relevance()` para:
- Agregar más contextos válidos
- Ajustar ejemplos de consultas válidas/inválidas
- Cambiar el tono del rechazo

## 🚀 Mejoras Futuras

1. **Cache de validaciones**: Guardar resultados de prompts comunes
2. **Lista blanca/negra**: Palabras clave para bypass o rechazo inmediato
3. **Métricas de uso**: Dashboard de consultas rechazadas
4. **Modo estricto/permisivo**: Configuración por usuario/institución
5. **Feedback del usuario**: "¿Esta respuesta fue útil?" para ajustar filtro

## 📚 Referencias

- Implementación: `app/graph/chatbot_graph.py`
- Tests: `test_security.py`
- Schema: `app/graph/schema/chat_state.py`

