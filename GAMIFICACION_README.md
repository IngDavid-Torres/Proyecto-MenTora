# Sistema de Gamificación - MenTora

Este documento explica el nuevo sistema de gamificación implementado en MenTora.

## 🎮 Características Implementadas

### 1. **Seguimiento Persistente de Progreso**
- Los puntos y logros se guardan en la base de datos permanentemente
- El progreso no se pierde al cerrar sesión
- Sistema de tracking para quizzes y juegos completados

### 2. **Sistema de Puntos**
- **Quizzes de Profesores**: 15 puntos por pregunta
- **Quizzes del Administrador**: 10 puntos por pregunta
- **Juegos**: 10 puntos por completar
- Los puntos solo se otorgan la primera vez que se completa una actividad

### 3. **Historial de Actividades**
- Registro completo de todas las actividades completadas
- Visualización en el dashboard con timestamps
- Estadísticas detalladas por tipo de actividad

### 4. **Sistema de Badges (Logros)**
Badges disponibles:
- 🏆 **Primer Quiz**: Completar 1 quiz
- 📚 **Maestro de Quizzes**: Completar 5 quizzes
- 🎮 **Primer Juego**: Completar 1 juego
- 🎯 **Jugador Experto**: Completar 5 juegos
- 💯 **100 Puntos**: Alcanzar 100 puntos
- ⭐ **500 Puntos**: Alcanzar 500 puntos
- 🔥 **Nivel 5**: Alcanzar el nivel 5
- 🌟 **Explorador**: Completar 10 actividades diferentes
- 📅 **Dedicado**: Completar actividades durante 7 días seguidos
- 👑 **Maestro MenTora**: Alcanzar el nivel 10

### 5. **Notificaciones y Alertas**
- Alertas visuales al ganar puntos
- Mensajes personalizados según el tipo de actividad
- Indicador de actividades ya completadas

## 📦 Instalación y Configuración

### Paso 1: Ejecutar las migraciones

```powershell
# Crear las nuevas tablas de gamificación
python migrate_gamification.py
```

### Paso 2: Inicializar los badges

```powershell
# Crear los badges predefinidos
python init_badges.py
```

### Paso 3: Reiniciar la aplicación

```powershell
# Detener procesos anteriores
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Esperar
Start-Sleep -Seconds 3

# Iniciar la aplicación
python app.py
```

## 🗄️ Nuevos Modelos de Base de Datos

### QuizProgress
Rastrea el progreso de cada usuario en cada quiz:
- `completed`: Si el quiz fue completado
- `score`: Número de respuestas correctas
- `total_questions`: Total de preguntas del quiz
- `points_earned`: Puntos ganados
- `attempts`: Número de intentos
- `last_attempt`: Fecha del último intento
- `completed_at`: Fecha de completación

### GameProgress
Rastrea el progreso de cada usuario en cada juego:
- `completed`: Si el juego fue completado
- `points_earned`: Puntos ganados
- `attempts`: Número de intentos
- `last_attempt`: Fecha del último intento
- `completed_at`: Fecha de completación

### ActivityLog
Registro histórico de todas las actividades:
- `activity_type`: Tipo de actividad (quiz, game, achievement)
- `activity_id`: ID de la actividad
- `activity_name`: Nombre de la actividad
- `points_earned`: Puntos ganados en esa actividad
- `description`: Descripción de la actividad
- `timestamp`: Fecha y hora del registro

## 🎯 Funcionalidades del Dashboard

### Estadísticas en Tiempo Real
- Total de quizzes completados
- Total de juegos completados
- Puntos totales de quizzes
- Puntos totales de juegos

### Historial de Actividades
- Lista cronológica de todas las actividades
- Iconos diferenciados por tipo de actividad
- Puntos ganados por cada actividad
- Fechas de completación

### Indicadores de Progreso
- Quizzes/juegos ya completados se marcan visualmente
- No se pueden ganar puntos duplicados
- Información de intentos y puntuación

## 🔧 Uso del Sistema

### Para Estudiantes

1. **Completar un Quiz**:
   - Responder todas las preguntas correctamente
   - Recibir puntos (primera vez solamente)
   - Ver el progreso guardado en el dashboard

2. **Completar un Juego**:
   - Resolver el desafío del juego
   - Recibir puntos (primera vez solamente)
   - Ver el logro en el historial

3. **Ver Progreso**:
   - Dashboard muestra todas las estadísticas
   - Historial completo de actividades
   - Badges desbloqueados

### Para Profesores/Administradores

- Los quizzes creados por profesores otorgan más puntos (15 vs 10)
- Pueden ver el progreso de los estudiantes
- Sistema de badges automático basado en logros

## 🚀 Próximas Mejoras Sugeridas

1. **Sistema de Racha**:
   - Contador de días consecutivos completando actividades
   - Bonificación por rachas largas

2. **Tabla de Líderes Mejorada**:
   - Filtros por período de tiempo
   - Rankings por área/curso

3. **Badges Personalizados**:
   - Los profesores pueden crear sus propios badges
   - Badges especiales por eventos

4. **Recompensas**:
   - Desbloquear contenido especial con puntos
   - Avatares premium
   - Temas personalizados

## 📝 Notas Técnicas

- Los puntos solo se otorgan una vez por actividad completada
- El sistema verifica automáticamente badges al completar actividades
- Todos los datos persisten en la base de datos PostgreSQL/SQLite
- Las sesiones solo almacenan información temporal (intentos, cooldowns)

## 🐛 Resolución de Problemas

### Los puntos no se guardan
- Verificar que las tablas fueron creadas: `python migrate_gamification.py`
- Verificar logs de errores en la consola

### Los badges no aparecen
- Ejecutar: `python init_badges.py`
- Verificar que la tabla `badges` existe

### El historial está vacío
- Solo muestra actividades completadas después de la migración
- Las actividades antiguas no se migran automáticamente
