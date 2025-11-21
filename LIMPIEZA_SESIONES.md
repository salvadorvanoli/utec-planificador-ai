# Sistema de Limpieza Automática de Sesiones

## 📋 Resumen
Se implementó un sistema robusto de limpieza automática de sesiones de chat para prevenir fugas de memoria en el servidor.

## 🔧 Cambios Implementados

### Archivo: `app/graph/utils.py`

#### Nuevas características:

1. **Thread de limpieza en segundo plano (Daemon)**
   - Se ejecuta automáticamente cada 5 minutos (300 segundos)
   - Es un thread daemon, por lo que se cierra automáticamente cuando la aplicación se detiene
   - No bloquea ni interfiere con las operaciones normales del servidor

2. **Constantes configurables:**
   ```python
   SESSION_TIMEOUT_MINUTES = 20  # Tiempo de inactividad antes de eliminar sesión
   CLEANUP_INTERVAL_SECONDS = 300  # Frecuencia de limpieza automática (5 min)
   ```

3. **Funciones nuevas:**
   - `cleanup_expired_sessions()`: Elimina todas las sesiones que superan el timeout
   - `background_cleanup_task()`: Tarea que corre en loop infinito en el thread daemon
   - `start_cleanup_thread()`: Inicia el thread de limpieza al cargar el módulo

4. **Logging mejorado:**
   - Registra cuando se crean nuevas sesiones
   - Registra cuando se eliminan sesiones expiradas
   - Registra el número total de sesiones eliminadas en cada limpieza

## 🎯 Funcionamiento

### Doble sistema de limpieza:

1. **Limpieza sincrónica (inmediata):**
   - Se ejecuta cada vez que se llama a `get_or_create_history()`
   - Elimina sesiones expiradas cuando un usuario envía un mensaje

2. **Limpieza asíncrona (en segundo plano):**
   - Thread daemon que corre cada 5 minutos
   - Elimina sesiones expiradas **incluso si ningún usuario envía mensajes**
   - **Soluciona el problema de sesiones huérfanas en RAM**

## 🔍 Ejemplo de Escenario

### Antes (Problema):
- Usuario A envía mensaje → sesión creada en RAM
- Usuario A nunca vuelve → sesión permanece en RAM indefinidamente
- Múltiples usuarios inactivos → fuga de memoria progresiva

### Después (Solución):
- Usuario A envía mensaje → sesión creada en RAM (timestamp guardado)
- Usuario A no envía nada por 20 minutos
- Thread de limpieza detecta inactividad (en el próximo ciclo de 5 min)
- Sesión eliminada automáticamente de RAM
- **Memoria liberada sin intervención manual**

## ⚙️ Configuración

Para ajustar los tiempos, modifica las constantes en `app/graph/utils.py`:

```python
SESSION_TIMEOUT_MINUTES = 20      # Cambiar timeout de sesión
CLEANUP_INTERVAL_SECONDS = 300    # Cambiar frecuencia de limpieza
```

## 🔒 Seguridad Thread-Safe

El sistema utiliza:
- Thread daemon (se cierra limpiamente con la aplicación)
- Operaciones atómicas en diccionarios de Python (thread-safe en CPython)
- Manejo de excepciones en el thread de limpieza para evitar crashes

## 📝 Logs de Ejemplo

```
2025-11-21 14:24:08 - app.graph.utils - INFO - Nueva sesión creada: user_123
2025-11-21 14:44:10 - app.graph.utils - INFO - Sesión expirada eliminada: user_123
2025-11-21 14:44:10 - app.graph.utils - INFO - Limpieza completada: 1 sesión(es) eliminada(s)
```

