
    // Variables globales del chatbot
    let chatbotOpen = false;
    let isTyping = false;
    let messageCount = 0;
    let isFirstMessage = true;

    // Base de conocimiento de MenTora
    const botResponses = {
        // === RESPUESTAS PRINCIPALES DE NAVEGACIÓN ===
        'como funciona': '**MenTora es una plataforma educativa gamificada donde los estudiantes aprenden de forma interactiva mediante juegos, retos y logros.**\n\n**¿Cómo funciona?**\n• **Resolver Retos Intelectuales:** Quiz interactivos en múltiples categorías (programación, matemáticas, ciencias, historia, literatura, tecnología)\n• **Sistema de Puntos:** Gana puntos por cada respuesta correcta y avanza en tu nivel\n• **Rankings Competitivos:** Compite con otros estudiantes y profesores en tiempo real\n• **Logros y Insignias:** Desbloquea badges especiales por tus logros académicos\n• **Biblioteca Digital:** Accede a recursos educativos organizados por temas\n• **Profesores Admin:** Los profesores pueden crear retos personalizados\n\n**"Gamifica tu aprendizaje"** significa que el aprendizaje se vuelve más divertido y motivante a través de dinámicas de juego, como niveles, puntos, retos y recompensas.',
        
        // === PREGUNTAS ESPECÍFICAS DE INICIO ===
        'que es mentora': '**MenTora es una plataforma educativa gamificada donde los estudiantes aprenden de forma interactiva mediante juegos, retos y logros.**\n\nTransformamos el aprendizaje tradicional en una experiencia emocionante donde cada respuesta correcta te acerca más a dominar nuevos conocimientos.\n\n**Características principales:**\n• Optimizada para dispositivos móviles\n• Acceso gratuito para estudiantes y profesores\n• Sistema de gamificación completo\n• Interacción en tiempo real\n• Biblioteca de recursos educativos\n\n¿Te gustaría saber cómo registrarte o qué puedes hacer en la plataforma?',

        'acceso gratuito': '**MenTora ofrece acceso completamente gratuito para estudiantes y profesores.**\n\nNo necesitas pagar nada para:\n• Crear tu cuenta y perfil\n• Acceder a todos los juegos y retos\n• Usar la biblioteca de recursos\n• Participar en rankings\n• Ganar logros y puntos\n• Chatear con la comunidad\n\nEn el futuro podríamos agregar funciones avanzadas premium, pero el núcleo de la plataforma siempre será gratuito.',

        'movil': '**La plataforma está completamente optimizada para dispositivos móviles.**\n\nPuedes usar MenTora desde:\n• Tu smartphone (Android/iOS)\n• Tu computadora o laptop\n• Tablet\n• Cualquier dispositivo con navegador web\n\n**Ventajas del diseño móvil:**\n• Interfaz responsive que se adapta a tu pantalla\n• Navegación táctil optimizada\n• Carga rápida incluso con conexión lenta\n• Todas las funciones disponibles en cualquier dispositivo',
        
        'que puedo hacer': '**En MenTora tienes muchas opciones:**\n\n**Sección "Aprende más":** Biblioteca digital con recursos de:\n• Python, JavaScript, Java, C++, HTML/CSS\n• Algoritmos y estructuras de datos\n• Patrones de diseño y APIs REST\n• Matemáticas, física, química\n• Historia, literatura y más\n\n**Juegos Educativos:** Retos interactivos creados por profesores\n\n**Tu Dashboard Personal:**\n• Ver tu progreso y nivel actual\n• Estadísticas de rendimiento\n• Historial de actividades\n• Ranking de líderes\n• Notificaciones importantes\n\n**Sistema de Logros:** Colecciona insignias por tus logros\n\n**Chat en Vivo:** Interactúa con otros estudiantes en tiempo real',

        'consejos estudio': '**Consejos personalizados para maximizar tu aprendizaje en MenTora:**\n\n**Organización:**\n• Establece sesiones de estudio de 25-30 minutos (Técnica Pomodoro)\n• Usa la biblioteca de MenTora para repasar antes de los retos\n• Revisa tu progreso diariamente en el dashboard\n\n**Estrategia de Juego:**\n• Empieza con retos básicos para ganar confianza\n• Enfócate en una categoría a la vez (ej: programación)\n• Participa en retos diarios para mantener racha\n• Usa el ranking como motivación sana\n\n**Para Programación:**\n• Practica con los recursos de Python, JavaScript y Java\n• Estudia algoritmos antes de intentar retos avanzados\n• Usa la sección de patrones de diseño\n\n**Comunidad:**\n• Participa en el chat en vivo para resolver dudas\n• Compite sanamente con compañeros\n• Comparte tus logros para mantener motivación',
        
        'registro': '**¿Cómo registrarse en MenTora?**\n\n**Opción 1:** Haz clic en el botón "Comenzar Gratis" en la página principal\n**Opción 2:** Usa el botón "Registrarse" en la esquina superior derecha\n\n**Proceso de registro:**\n**Paso 1:** Completa tus datos básicos:\n• Nombre de usuario único\n• Email válido (recibirás confirmación)\n• Contraseña segura (mín. 8 caracteres)\n\n**Paso 2:** Elige tu rol:\n• **Estudiante** - Acceso a juegos, retos y biblioteca\n• **Profesor** - Panel administrativo + funciones de estudiante\n\n**Paso 3:** Personaliza tu perfil y avatar\n\n**Al completar el registro tendrás acceso inmediato a:**\n• Dashboard personal con estadísticas\n• Biblioteca de recursos educativos\n• Primer reto de bienvenida\n• Sistema de puntos iniciado en 0\n• Chat en vivo con la comunidad\n\nEs completamente gratis y toma menos de 2 minutos.',

        'login': '**Proceso de inicio de sesión:**\n\n1. **Clic en "Iniciar Sesión"** (navbar superior derecho)\n2. **Ingresa credenciales:** Usuario y contraseña\n3. **Bienvenido a tu dashboard** Donde verás:\n\n**Panel Principal:**\n• Puntos actuales y nivel\n• Progreso hacia siguiente nivel\n• Logros desbloqueados recientes\n• Ranking actual entre usuarios\n\n**Reto Especial del Día:** Desafío diario con puntos extra\n\n**Notificaciones:** Mensajes importantes del sistema\n\n**Historial:** Tus actividades recientes\n\n**¿Olvidaste tu contraseña?** Usa la opción de recuperación en la página de login',
        
        // === RESPUESTAS ESPECIALIZADAS POR ÁREA ===
        'programacion': '**Sección de Programación en MenTora:**\n\n**Biblioteca de Recursos (12 recursos disponibles):**\n• **Python para Principiantes:** Variables, funciones, bucles, estructuras de datos\n• **JavaScript ES6+ Moderno:** Arrow functions, async/await, destructuring\n• **Java Fundamentos:** POO, herencia, polimorfismo, interfaces\n• **C++ Avanzado:** Punteros, memoria dinámica, templates, STL\n• **Algoritmos y Estructuras de Datos:** Arrays, listas, pilas, árboles\n• **HTML5 y CSS3:** Responsive design, flexbox, grid\n• **React.js:** Componentes, hooks, contexto\n• **APIs REST y Flask:** Desarrollo de servicios web\n• **Git y Control de Versiones:** Branching, merging, GitHub\n• **Patrones de Diseño:** Singleton, Factory, Observer\n• **Testing y Depuración:** Unit testing, TDD\n• **SQL y Bases de Datos:** Consultas, joins, optimización\n\n**Retos de Programación:**\n• Preguntas sobre sintaxis y conceptos\n• Análisis de algoritmos y complejidad\n• Debugging y resolución de problemas\n• Mejores prácticas y patrones',

        'matematicas': '**Matemáticas en MenTora:**\n\n**Recursos Disponibles:**\n• **Álgebra Lineal Básica:** Vectores, matrices, operaciones\n• **Cálculo Diferencial:** Límites, derivadas, aplicaciones\n• **Estadística y Probabilidad:** Distribuciones, análisis de datos\n• **Matemáticas Discretas:** Lógica, combinatoria, grafos\n• **Geometría Analítica:** Coordenadas, ecuaciones de rectas\n\n**Tipos de Retos:**\n• Problemas de cálculo paso a paso\n• Aplicaciones prácticas en programación\n• Análisis de algoritmos (Big O)\n• Probabilidad en ciencias computacionales\n\n**Tips:**\n• Practica con calculadoras interactivas\n• Revisa fórmulas antes de los retos\n• Conecta matemáticas con programación',
        
        'biblioteca': '**Biblioteca Digital de MenTora - Tu Centro de Aprendizaje:**\n\n**Búsqueda Inteligente:**\n• Busca por tema, tecnología o nivel\n• Filtros por categoría (programación, matemáticas, etc.)\n• Sugerencias automáticas\n\n**Categorías Principales:**\n• **Programación (12 recursos):** Desde Python básico hasta patrones avanzados\n• **Matemáticas (8 recursos):** Álgebra, cálculo, estadística\n• **Ciencias (6 recursos):** Física, química, biología\n• **Historia (5 recursos):** Mundial, culturas, civilizaciones\n• **Literatura (7 recursos):** Análisis de obras clásicas\n• **Tecnología (9 recursos):** IA, blockchain, tendencias\n\n**Características:**\n• Contenido interactivo con ejemplos\n• Niveles: Básico, Intermedio, Avanzado\n• Tiempo estimado de estudio\n• Recursos descargables\n• Actualizaciones constantes',

        'dashboard': '**Tu Dashboard Personal - Centro de Control:**\n\n**¿Cómo gano puntos en MenTora?**\nGanas puntos completando juegos, retos y quizzes. También puedes recibir puntos extra por participar activamente en actividades especiales.\n\n**¿Qué significa mi nivel?**\nTu nivel refleja tu progreso general en la plataforma. A medida que acumulas puntos, tu nivel aumenta automáticamente.\n\n**¿Dónde puedo ver mis logros?**\nTus logros se muestran en la sección "Logros" dentro del dashboard. Cada logro representa un hito importante en tu aprendizaje.\n\n**¿Qué es el "Reto Especial del Día"?**\nEs una actividad única disponible por tiempo limitado para ganar puntos y recompensas adicionales. Renueva cada 24 horas.\n\n**¿Cómo funciona el ranking de líderes?**\nEl ranking muestra a los estudiantes con más puntos y niveles dentro de la plataforma. Es una forma divertida de competir sanamente.\n\n**¿Cómo puedo hablar con un profesor?**\nPuedes usar el botón de chat en vivo para comunicarte con un profesor o soporte técnico en tiempo real.\n\n**¿Cómo cambio mi avatar o nombre?**\nHaz clic en "Editar Perfil" desde el menú del usuario en la esquina superior derecha.\n\n**¿Qué pasa si cierro sesión?**\nPerderás el acceso al panel y deberás iniciar sesión de nuevo para continuar. Tus datos y progreso se guardan automáticamente.',
        
        'juegos': '**Sección de Juegos y Retos:**\n\n**Tipos de Contenido:**\n• **Quiz Interactivos:** Preguntas de opción múltiple\n• **Retos de Programación:** Ejercicios de código\n• **Juegos Educativos:** Creados por profesores\n• **Desafíos Colaborativos:** Trabajo en equipo\n\n**Características:**\n• **Sistema de Puntos:** Gana puntos por respuestas correctas\n• **Cronómetro:** Retos contra tiempo\n• **Múltiples Intentos:** Practica hasta dominar\n• **Retroalimentación:** Explicaciones de respuestas\n\n**Logros Especiales:**\n• Racha de respuestas correctas\n• Completar categorías específicas\n• Participación en retos diarios\n• Tiempo récord en resolución\n\n**Integración con Biblioteca:** Estudia antes de jugar para mejores resultados',

        'profesores': '**Panel del Profesor - Gestión Educativa Completa:**\n\n**¿Qué puedo hacer desde el panel de profesor?**\nPuedes gestionar tus quizzes, juegos creados y consultar el desempeño detallado de tus alumnos en tiempo real.\n\n**¿Cómo agrego un nuevo quiz?**\nEn la sección "Mis Quizzes", usa el botón "Agregar Quiz" para crear uno nuevo. Incluye preguntas, respuestas y nivel de dificultad.\n\n**¿Dónde veo los resultados de mis alumnos?**\nEn la tabla de "Alumnos inscritos en tu área" podrás consultar sus puntajes, correos y progreso individual.\n\n**¿Puedo modificar un quiz existente?**\nSí, selecciona el quiz que desees editar y usa el botón de edición correspondiente. Puedes cambiar preguntas, respuestas y configuraciones.\n\n**¿Qué significa el área del profesor?**\nCada profesor pertenece a un área temática (por ejemplo, matemáticas, tecnología o inglés) y solo ve alumnos asociados a esa área específica.\n\n**¿Puedo comunicarme con mis alumnos?**\nSí, puedes usar el chat integrado o las funciones de comunicación dentro del dashboard para contactar estudiantes.\n\n**¿Qué pasa si cierro sesión?**\nTu sesión se cerrará y deberás volver a iniciar sesión con tu cuenta de profesor. Todos tus datos se guardan automáticamente.\n\n**Herramientas adicionales:**\n• Sistema de logros personalizables\n• Estadísticas detalladas de rendimiento\n• Generación automática de contenido con IA\n• Exportación de reportes y exámenes',
        
        'ayuda': '**Centro de Ayuda MenTora:**\n\n**Soporte Técnico:**\n• **Chat en Vivo:** Habla con otros usuarios en tiempo real\n• **MenToraBot:** Asistente 24/7\n• **Email Soporte:** Para problemas técnicos complejos\n\n**Preguntas Frecuentes:**\n• ¿Cómo restablecer contraseña?\n• ¿Cómo subir de nivel más rápido?\n• ¿Qué hacer si un reto no carga?\n• ¿Cómo acceder a recursos premium?\n\n**Guías de Usuario:**\n• Tutorial de inicio para nuevos usuarios\n• Guía avanzada de la biblioteca\n• Manual para profesores\n• Mejores prácticas de estudio\n\n**Reportar Problemas:**\n• Bugs en la plataforma\n• Contenido incorrecto\n• Sugerencias de mejora\n• Solicitudes de nuevas funciones',

        'tecnologia': '**Sección de Tecnología Avanzada:**\n\n**Inteligencia Artificial:**\n• Fundamentos de Machine Learning\n• Redes neuronales básicas\n• Aplicaciones en la vida cotidiana\n• Ética en IA\n\n**Blockchain y Criptomonedas:**\n• Conceptos básicos de blockchain\n• Smart contracts\n• NFTs y aplicaciones\n\n**Cloud Computing:**\n• AWS, Azure, Google Cloud\n• Servicios en la nube\n• DevOps y deployment\n\n**Desarrollo Móvil:**\n• React Native\n• Flutter\n• Ionic\n• App Store optimization',

        // === NUEVAS PREGUNTAS FRECUENTES ===
        'como recuperar contrasena': '**Recuperación de Contraseña:**\n\n**Pasos para restablecer tu contraseña:**\n1. Ve a la página de inicio de sesión\n2. Haz clic en "¿Olvidaste tu contraseña?"\n3. Ingresa tu email registrado\n4. Recibirás un correo con un enlace de recuperación\n5. Haz clic en el enlace (válido por 24 horas)\n6. Crea una nueva contraseña segura\n\n**Requisitos de contraseña:**\n• Mínimo 8 caracteres\n• Combinación de letras y números\n• Al menos una letra mayúscula\n\n**¿No recibes el correo?**\n• Revisa tu carpeta de spam\n• Verifica que el email sea correcto\n• Espera unos minutos e intenta de nuevo\n• Contacta a soporte si persiste el problema',

        'cambiar contrasena': '**Cambiar Contraseña desde tu Perfil:**\n\n**Pasos:**\n1. Inicia sesión en tu cuenta\n2. Ve a tu perfil (icono de usuario en la esquina superior derecha)\n3. Selecciona "Configuración" o "Editar Perfil"\n4. Busca la sección "Seguridad"\n5. Haz clic en "Cambiar Contraseña"\n6. Ingresa tu contraseña actual\n7. Escribe tu nueva contraseña\n8. Confirma la nueva contraseña\n9. Guarda los cambios\n\n**Recomendaciones de seguridad:**\n• Cambia tu contraseña cada 3-6 meses\n• No uses la misma contraseña en múltiples sitios\n• Usa una combinación única de caracteres',

        'niveles': '**Sistema de Niveles en MenTora:**\n\n**¿Cómo funcionan los niveles?**\nTu nivel aumenta automáticamente conforme acumulas puntos. Hay 100 niveles en total con progresión exponencial.\n\n**Rangos de niveles:**\n• **Nivel 1-20:** Principiante (0-1000 puntos)\n• **Nivel 21-40:** Intermedio (1001-5000 puntos)\n• **Nivel 41-60:** Avanzado (5001-15000 puntos)\n• **Nivel 61-80:** Experto (15001-35000 puntos)\n• **Nivel 81-100:** Maestro (35001+ puntos)\n\n**Beneficios por nivel:**\n• Desbloqueo de retos más difíciles\n• Acceso a contenido exclusivo\n• Insignias especiales por hito\n• Mayor visibilidad en rankings\n• Reconocimiento en la comunidad',

        'puntos': '**Sistema de Puntos en MenTora:**\n\n**¿Cómo ganar puntos?**\n• **Respuestas correctas:** 10-50 puntos por pregunta (según dificultad)\n• **Reto diario completado:** 100 puntos bonus\n• **Racha de respuestas:** +5 puntos por cada respuesta consecutiva correcta\n• **Tiempo récord:** 20-30 puntos extra\n• **Completar categoría:** 200 puntos\n• **Participación en chat:** 5 puntos por mensaje constructivo\n\n**Multiplicadores:**\n• Nivel Fácil: 1x puntos\n• Nivel Medio: 2x puntos\n• Nivel Difícil: 3x puntos\n• Modo Experto: 5x puntos\n\n**¿Puedo perder puntos?**\nNo. En MenTora no pierdes puntos, solo los acumulas progresivamente.',

        'insignias': '**Sistema de Insignias y Logros:**\n\n**Categorías de insignias:**\n\n**Logros de Aprendizaje:**\n• Primera Victoria: Completa tu primer reto\n• Estudioso: 10 retos completados\n• Maestro del Conocimiento: 100 retos completados\n\n**Logros de Especialización:**\n• Programador: 50 retos de programación\n• Matemático: 50 retos de matemáticas\n• Científico: 50 retos de ciencias\n\n**Logros Sociales:**\n• Comunicador: 100 mensajes en chat\n• Mentor: Ayuda a 10 estudiantes\n• Líder: Alcanza el top 10 del ranking\n\n**Logros Especiales:**\n• Racha de Fuego: 7 días consecutivos activo\n• Perfeccionista: 20 retos con 100% de aciertos\n• Velocista: Completa un reto en tiempo récord\n\n**¿Cómo ver mis insignias?**\nEn tu dashboard, sección "Logros" podrás ver todas tus insignias desbloqueadas y las que están por conseguir.',

        'ranking': '**Sistema de Rankings:**\n\n**Tipos de rankings:**\n\n**Ranking Global:**\n• Muestra a los top 100 usuarios con más puntos\n• Se actualiza en tiempo real\n• Incluye estudiantes y profesores\n\n**Ranking por Categoría:**\n• Programación\n• Matemáticas\n• Ciencias\n• Historia\n• Literatura\n• Tecnología\n\n**Ranking Semanal:**\n• Se reinicia cada lunes\n• Premia a los usuarios más activos de la semana\n\n**Ranking Mensual:**\n• Competencia mensual\n• Los 3 primeros lugares reciben insignias especiales\n\n**¿Cómo subir en el ranking?**\n• Completa más retos diarios\n• Mantén una racha activa\n• Participa en todas las categorías\n• Responde con precisión y velocidad',

        'retos diarios': '**Retos Diarios:**\n\n**¿Qué son los retos diarios?**\nSon desafíos especiales que cambian cada 24 horas y ofrecen recompensas extra.\n\n**Características:**\n• Disponible desde las 00:00 hasta las 23:59\n• Diferente dificultad cada día\n• Bonus de 100 puntos al completar\n• Cuenta para tu racha diaria\n\n**Tipos de retos diarios:**\n• Lunes: Programación\n• Martes: Matemáticas\n• Miércoles: Ciencias\n• Jueves: Tecnología\n• Viernes: Mix de categorías\n• Sábado: Reto comunidad\n• Domingo: Mega reto (puntos dobles)\n\n**Sistema de rachas:**\n• 7 días consecutivos: Insignia "Racha de Fuego"\n• 30 días consecutivos: Insignia "Dedicación"\n• 90 días consecutivos: Insignia "Leyenda"',

        'chat comunidad': '**Chat en Vivo de la Comunidad:**\n\n**¿Cómo funciona?**\nEl chat en vivo te permite interactuar con otros estudiantes y profesores en tiempo real.\n\n**Características:**\n• Mensajes instantáneos\n• Sistema de moderación automática\n• Emojis y formato de texto\n• Notificaciones de mensajes\n\n**Reglas del chat:**\n• Respeto mutuo siempre\n• No spam ni contenido inapropiado\n• Mantén conversaciones constructivas\n• Comparte conocimiento, no respuestas directas\n\n**Funciones especiales:**\n• Mencionar usuarios con @usuario\n• Crear grupos de estudio\n• Compartir recursos educativos\n• Pedir ayuda a profesores\n\n**Reportar problemas:**\nSi ves comportamiento inapropiado, usa el botón "Reportar" junto al mensaje.',

        'perfil': '**Personalización de Perfil:**\n\n**¿Qué puedo personalizar?**\n\n**Información básica:**\n• Nombre de usuario (único)\n• Avatar o foto de perfil\n• Biografía corta (150 caracteres)\n• País y ciudad\n\n**Preferencias:**\n• Categorías favoritas\n• Nivel de dificultad preferido\n• Idioma de la interfaz\n• Zona horaria\n\n**Privacidad:**\n• Visibilidad de perfil (público/privado)\n• Mostrar/ocultar estadísticas\n• Permitir mensajes directos\n• Mostrar en ranking\n\n**Estadísticas visibles:**\n• Total de puntos\n• Nivel actual\n• Insignias desbloqueadas\n• Retos completados\n• Racha actual\n\n**¿Cómo editar mi perfil?**\nHaz clic en tu avatar (esquina superior derecha) → Editar Perfil',

        'notificaciones': '**Sistema de Notificaciones:**\n\n**Tipos de notificaciones:**\n\n**Notificaciones de Logros:**\n• Nueva insignia desbloqueada\n• Subiste de nivel\n• Nuevo récord personal\n\n**Notificaciones Sociales:**\n• Nuevo mensaje en el chat\n• Alguien te mencionó\n• Invitación a grupo de estudio\n\n**Notificaciones del Sistema:**\n• Nuevo reto diario disponible\n• Tu racha está por romperse\n• Nuevo contenido en la biblioteca\n• Actualización de la plataforma\n\n**Configurar notificaciones:**\n• Ve a Configuración → Notificaciones\n• Activa/desactiva por tipo\n• Elige recibir por email o solo en plataforma\n• Configura horario de no molestar',

        'categorias': '**Categorías de Contenido:**\n\n**Todas las categorías disponibles:**\n\n**Programación:**\n• Python, JavaScript, Java, C++\n• Algoritmos y estructuras de datos\n• Desarrollo web y móvil\n• Bases de datos\n\n**Matemáticas:**\n• Álgebra y cálculo\n• Estadística y probabilidad\n• Geometría\n• Matemáticas discretas\n\n**Ciencias:**\n• Física\n• Química\n• Biología\n\n**Humanidades:**\n• Historia mundial\n• Literatura clásica y contemporánea\n• Filosofía\n\n**Tecnología:**\n• Inteligencia Artificial\n• Cloud Computing\n• Blockchain\n• Ciberseguridad\n\n**Idiomas:**\n• Inglés\n• Francés\n• Alemán\n\n**¿Cómo elegir una categoría?**\nEn tu dashboard o en la sección "Juegos", filtra por la categoría de tu interés.',

        'progreso': '**Seguimiento de Progreso:**\n\n**¿Dónde veo mi progreso?**\nEn tu dashboard personal encontrarás estadísticas detalladas.\n\n**Métricas principales:**\n\n**Rendimiento General:**\n• Total de puntos acumulados\n• Nivel actual y progreso al siguiente\n• Porcentaje de retos completados\n• Tasa de aciertos\n\n**Análisis por Categoría:**\n• Puntos por categoría\n• Tiempo invertido\n• Retos completados vs. disponibles\n• Fortalezas y áreas de mejora\n\n**Gráficos y estadísticas:**\n• Evolución de puntos (últimos 30 días)\n• Actividad semanal\n• Comparativa con otros usuarios\n• Heatmap de estudio\n\n**Exportar progreso:**\nPuedes descargar un reporte PDF de tu progreso mensual desde Configuración → Reportes.',

        'dificultad': '**Niveles de Dificultad:**\n\n**¿Cómo funciona la dificultad?**\nCada reto tiene un nivel de dificultad asignado:\n\n**Fácil (Verde):**\n• Para principiantes\n• 5-10 preguntas\n• 10 puntos por pregunta\n• Sin límite de tiempo\n\n**Medio (Amarillo):**\n• Nivel intermedio\n• 10-15 preguntas\n• 20 puntos por pregunta\n• 15 minutos límite\n\n**Difícil (Naranja):**\n• Nivel avanzado\n• 15-20 preguntas\n• 30 puntos por pregunta\n• 10 minutos límite\n\n**Experto (Rojo):**\n• Nivel profesional\n• 20-25 preguntas\n• 50 puntos por pregunta\n• 8 minutos límite\n\n**Recomendación:**\nEmpieza con el nivel fácil y avanza gradualmente. El sistema también te sugerirá niveles según tu rendimiento.',

        // === RESPUESTA POR DEFECTO EXPANDIDA ===
        'default': '**Como MenToraBot, el asistente oficial de la plataforma, puedo ayudarte con:**\n\n**ARQUITECTURA Y TECNOLOGÍA:**\n• Detalles técnicos: Flask, SQLAlchemy, Socket.IO, WebSockets\n• 10+ tablas de base de datos con relaciones complejas\n• APIs REST completas y endpoints especializados\n• Sistema de autenticación y seguridad avanzado\n• Integración de IA local para generación automática\n\n**SISTEMA EDUCATIVO COMPLETO:**\n• Quiz interactivos con múltiples tipos de pregunta\n• Biblioteca digital: 47+ recursos en 6 categorías principales\n• Sistema de juegos: programación, lógica, colaborativos\n• Generación automática de exámenes exportables\n• Analytics detallado de rendimiento estudiantil\n\n**GAMIFICACIÓN AVANZADA:**\n• 100 niveles con progresión exponencial balanceada\n• 50+ logros en 6 categorías diferentes\n• Sistema de puntos con múltiples fuentes\n• Rankings globales y por especialización\n• Eventos especiales y competencias estacionales\n\n**GESTIÓN DE USUARIOS:**\n• Roles granulares: estudiante/profesor/admin\n• Perfiles completamente personalizables\n• Sistema de permisos y moderación automática\n• Herramientas administrativas completas\n• Analytics y reportes institucionales\n\n**COMUNICACIÓN EN TIEMPO REAL:**\n• Chat con WebSockets y moderación IA\n• Sistema de notificaciones inteligente\n• Mensajes multimedia y formato rico\n• Grupos de estudio y mentorías\n\n**HERRAMIENTAS PARA PROFESORES:**\n• Panel administrativo con 15+ funcionalidades\n• Creación de contenido con editor visual\n• Sistema de logros personalizable\n• Estadísticas detalladas de estudiantes\n• Generación automática con IA local\n\nTengo conocimiento exhaustivo de cada funcionalidad y proceso de MenTora. Pregúntame lo que necesites.'
    };

    // Función para alternar el chatbot
    function toggleChatbot() {
        const box = document.getElementById('chatbot-box');
        const btn = document.getElementById('chatbot-toggle');
        const notificationDot = document.getElementById('notificationDot');
        
        if (!chatbotOpen) {
            box.style.display = 'flex';
            btn.style.display = 'none';
            chatbotOpen = true;
            notificationDot.style.display = 'none';
            
            // Focus en el input
            setTimeout(() => {
                document.getElementById('chatbot-input').focus();
            }, 300);
        } else {
            box.style.display = 'none';
            btn.style.display = 'flex';
            chatbotOpen = false;
        }
    }

    // Función para limpiar el chat
    function clearChat() {
        const messages = document.getElementById('chatbot-messages');
        const welcomeMessage = messages.querySelector('.welcome-message');
        messages.innerHTML = '';
        messages.appendChild(welcomeMessage);
        messageCount = 0;
        isFirstMessage = true; // Resetear flag de primer mensaje

        // Mostrar sugerencias nuevamente
        document.getElementById('quickSuggestions').style.display = 'flex';
    }

    // Función para enviar mensajes rápidos
    function sendQuickMessage(message) {
        document.getElementById('chatbot-input').value = message;
        sendChatbotMessage(new Event('submit'));
    }

    // Función principal para enviar mensajes
    async function sendChatbotMessage(e) {
        e.preventDefault();
        
        if (isTyping) return;
        
        const input = document.getElementById('chatbot-input');
        const messages = document.getElementById('chatbot-messages');
        const sendBtn = document.querySelector('.send-btn');
        const userMsg = input.value.trim();
        
        if (!userMsg) return;
        
        // Ocultar sugerencias después del primer mensaje
        if (messageCount === 0) {
            document.getElementById('quickSuggestions').style.display = 'none';
        }
        
        messageCount++;
        
        // Agregar mensaje del usuario
        addUserMessage(userMsg);
        
        // Limpiar input y deshabilitar botón
        input.value = '';
        sendBtn.disabled = true;
        
        // Mostrar indicador de escritura
        showTypingIndicator();
        
        // Generar respuesta del bot
        setTimeout(async () => {
            hideTypingIndicator();
            
            // Usar siempre respuesta local para mayor confiabilidad
            console.log('Procesando mensaje:', userMsg);
            const localResponse = getLocalResponse(userMsg);
            console.log('Respuesta generada:', localResponse.substring(0, 100) + '...');
            addBotMessage(localResponse);
            
            sendBtn.disabled = false;
        }, Math.random() * 1000 + 800); // Simular tiempo de respuesta humano
    }

    // Función para obtener respuesta local enriquecida
    function getLocalResponse(message) {
        const msg = message.toLowerCase().trim();
        console.log('🔍 Analizando mensaje:', msg);

        // === RESPUESTAS DIRECTAS SIMPLES ===

        // Saludos - Solo presentación completa en el primer mensaje
        if (msg.includes('hola') || msg.includes('hello') || msg.includes('hey') || msg.includes('buenos')) {
            if (isFirstMessage) {
                isFirstMessage = false;
                const hora = new Date().getHours();
                let saludo = 'Hola';
                if (hora >= 6 && hora < 12) saludo = 'Buenos días';
                else if (hora >= 12 && hora < 18) saludo = 'Buenas tardes';
                else if (hora >= 18 || hora < 6) saludo = 'Buenas noches';

                return `**${saludo}. Soy MenToraBot, tu asistente personal en la plataforma.**\n\n¿En qué puedo ayudarte hoy? Puedes preguntarme sobre:\n• Cómo usar la biblioteca de recursos\n• Juegos y retos disponibles\n• Tu progreso y estadísticas\n• Recursos de programación\n• Materiales de matemáticas\n• Sistema de logros y niveles\n• Chat en vivo con la comunidad\n\nEstoy aquí para hacer tu experiencia en MenTora más eficiente.`;
            } else {
                return '**Hola de nuevo.** ¿En qué más puedo ayudarte?';
            }
        }
        
        // Marcar que ya no es el primer mensaje para cualquier pregunta específica
        isFirstMessage = false;

        // ¿Qué es MenTora?
        if (msg.includes('que es mentora') || msg.includes('que es la plataforma') || msg.includes('explicame mentora')) {
            console.log('Detectado: que es mentora');
            return botResponses['que es mentora'];
        }

        // ¿Es gratis? / Precio
        if (msg.includes('es gratis') || msg.includes('gratis') || msg.includes('pagar') || msg.includes('costo') || msg.includes('precio') || msg.includes('gratuito')) {
            console.log(' Detectado: acceso gratuito');
            return botResponses['acceso gratuito'];
        }

        // ¿Cómo gano puntos?
        if (msg.includes('como gano puntos') || msg.includes('ganar puntos') || msg.includes('conseguir puntos')) {
            console.log(' Detectado: como gano puntos');
            return botResponses.dashboard;
        }

        // ¿Cómo funciona?
        if (msg.includes('como funciona') || msg.includes('explicame') || msg.includes('gamifica')) {
            console.log(' Detectado: como funciona');
            return botResponses['como funciona'];
        }

        // ¿Qué puedo hacer?
        if (msg.includes('que puedo hacer') || msg.includes('que hay') || msg.includes('funcionalidades')) {
            console.log(' Detectado: que puedo hacer');
            return botResponses['que puedo hacer'];
        }

        // Móvil / Dispositivos
        if (msg.includes('movil') || msg.includes('telefono') || msg.includes('celular') || msg.includes('dispositivo') || msg.includes('tablet')) {
            console.log('Detectado: movil');
            return botResponses['movil'];
        }

        // Ayuda
        if (msg.includes('ayuda') || msg.includes('help') || msg.includes('auxilio')) {
            console.log('Detectado: ayuda');
            return botResponses.ayuda;
        }

        // Consejos
        if (msg.includes('consejos') || msg.includes('tips') || msg.includes('recomendaciones')) {
            console.log('Detectado: consejos');
            return botResponses['consejos estudio'];
        }

        // Programación
        if (msg.includes('programacion') || msg.includes('codigo') || msg.includes('python') || msg.includes('javascript')) {
            console.log('Detectado: programacion');
            return botResponses.programacion;
        }

        // Matemáticas
        if (msg.includes('matematicas') || msg.includes('mates') || msg.includes('calculo')) {
            console.log('Detectado: matematicas');
            return botResponses.matematicas;
        }

        // Biblioteca
        if (msg.includes('biblioteca') || msg.includes('recursos') || msg.includes('materiales')) {
            console.log('Detectado: biblioteca');
            return botResponses.biblioteca;
        }
        
        // Dashboard y preguntas específicas de estudiantes
        if (msg.includes('dashboard') || msg.includes('progreso') || msg.includes('como gano puntos') || 
            msg.includes('que significa mi nivel') || msg.includes('donde veo logros') || 
            msg.includes('reto especial') || msg.includes('ranking') || msg.includes('chat profesor') ||
            msg.includes('cambio avatar') || msg.includes('editar perfil') || msg.includes('cierro sesion')) {
            console.log('Detectado: dashboard');
            return botResponses.dashboard;
        }
        
        // Preguntas específicas de puntos y niveles
        if (msg.includes('ganar puntos') || msg.includes('como subo nivel') || msg.includes('puntos extra')) {
            console.log('Detectado: dashboard (puntos)');
            return botResponses.dashboard;
        }
        
        // Logros y ranking
        if (msg.includes('logros') || msg.includes('ranking') || msg.includes('lider') || msg.includes('posicion')) {
            console.log('Detectado: dashboard (logros)');
            return botResponses.dashboard;
        }
        
        // Juegos
        if (msg.includes('juegos') || msg.includes('retos') || msg.includes('quiz')) {
            console.log('Detectado: juegos');
            return botResponses.juegos;
        }
        
        // Profesores y panel docente
        if (msg.includes('profesor') || msg.includes('admin') || msg.includes('docente') ||
            msg.includes('panel profesor') || msg.includes('agregar quiz') || msg.includes('crear quiz') ||
            msg.includes('resultados alumnos') || msg.includes('modificar quiz') || msg.includes('area profesor') ||
            msg.includes('comunicarme alumnos') || msg.includes('gestionar') || msg.includes('ensenar')) {
            console.log('Detectado: profesores');
            return botResponses.profesores;
        }
        
        // Específico para gestión de quizzes
        if (msg.includes('quiz') && (msg.includes('crear') || msg.includes('editar') || msg.includes('modificar'))) {
            console.log('Detectado: profesores (quiz)');
            return botResponses.profesores;
        }
        
        // Registro
        if (msg.includes('registro') || msg.includes('registrarme') || msg.includes('crear cuenta')) {
            console.log('Detectado: registro');
            return botResponses.registro;
        }
        
        // Login
        if (msg.includes('login') || msg.includes('iniciar sesion') || msg.includes('entrar')) {
            console.log('Detectado: login');
            return botResponses.login;
        }
        
        // Tecnología
        if (msg.includes('tecnologia') || msg.includes('inteligencia artificial') || msg.includes('blockchain')) {
            console.log('Detectado: tecnologia');
            return botResponses.tecnologia;
        }

        // === NUEVAS DETECCIONES ===

        // Recuperar contraseña
        if (msg.includes('recuperar contrasena') || msg.includes('olvide contrasena') || msg.includes('olvide mi contrasena') ||
            msg.includes('restablecer contrasena') || msg.includes('resetear contrasena')) {
            console.log('Detectado: recuperar contrasena');
            return botResponses['como recuperar contrasena'];
        }

        // Cambiar contraseña
        if (msg.includes('cambiar contrasena') || msg.includes('modificar contrasena') || msg.includes('actualizar contrasena')) {
            console.log('Detectado: cambiar contrasena');
            return botResponses['cambiar contrasena'];
        }

        // Niveles
        if (msg.includes('niveles') || msg.includes('que nivel') || msg.includes('subir nivel') ||
            msg.includes('como subir de nivel') || msg.includes('sistema de niveles')) {
            console.log('Detectado: niveles');
            return botResponses.niveles;
        }

        // Puntos específicos
        if (msg.includes('sistema de puntos') || msg.includes('como funcionan los puntos') ||
            msg.includes('cuantos puntos') || msg.includes('perder puntos')) {
            console.log('Detectado: puntos');
            return botResponses.puntos;
        }

        // Insignias
        if (msg.includes('insignias') || msg.includes('badges') || msg.includes('medallas') ||
            msg.includes('como conseguir insignias') || msg.includes('logros especiales')) {
            console.log('Detectado: insignias');
            return botResponses.insignias;
        }

        // Ranking específico
        if (msg.includes('como funciona el ranking') || msg.includes('tipos de ranking') ||
            msg.includes('ranking semanal') || msg.includes('ranking mensual') || msg.includes('subir en ranking')) {
            console.log('Detectado: ranking');
            return botResponses.ranking;
        }

        // Retos diarios
        if (msg.includes('reto diario') || msg.includes('retos diarios') || msg.includes('desafio diario') ||
            msg.includes('racha') || msg.includes('racha diaria')) {
            console.log('Detectado: retos diarios');
            return botResponses['retos diarios'];
        }

        // Chat comunidad
        if (msg.includes('chat') || msg.includes('chat en vivo') || msg.includes('chat comunidad') ||
            msg.includes('hablar con otros') || msg.includes('comunidad')) {
            console.log('Detectado: chat comunidad');
            return botResponses['chat comunidad'];
        }

        // Perfil y personalización
        if (msg.includes('perfil') || msg.includes('personalizar perfil') || msg.includes('editar perfil') ||
            msg.includes('cambiar avatar') || msg.includes('mi perfil')) {
            console.log('Detectado: perfil');
            return botResponses.perfil;
        }

        // Notificaciones
        if (msg.includes('notificaciones') || msg.includes('notificacion') || msg.includes('alertas') ||
            msg.includes('configurar notificaciones')) {
            console.log('Detectado: notificaciones');
            return botResponses.notificaciones;
        }

        // Categorías
        if (msg.includes('categorias') || msg.includes('que categorias') || msg.includes('tipos de contenido') ||
            msg.includes('areas de estudio')) {
            console.log('Detectado: categorias');
            return botResponses.categorias;
        }

        // Progreso
        if (msg.includes('mi progreso') || msg.includes('ver progreso') || msg.includes('estadisticas') ||
            msg.includes('seguimiento') || msg.includes('metricas')) {
            console.log('Detectado: progreso');
            return botResponses.progreso;
        }

        // Dificultad
        if (msg.includes('dificultad') || msg.includes('niveles de dificultad') || msg.includes('facil medio dificil') ||
            msg.includes('que dificultad') || msg.includes('nivel experto')) {
            console.log('Detectado: dificultad');
            return botResponses.dificultad;
        }

        // Agradecimientos
        if (msg.includes('gracias') || msg.includes('excelente') || msg.includes('perfecto')) {
            return '**De nada. Es un placer ayudarte.**\n\nComo asistente de MenTora, mi objetivo es hacer tu experiencia de aprendizaje lo más fluida posible.\n\n¿Hay algo más en lo que pueda asistirte? Puedo ayudarte con:\n• Encontrar recursos específicos\n• Optimizar tu progreso\n• Estrategias de estudio\n• Recomendaciones de retos';
        }

        // Despedidas
        if (msg.includes('adios') || msg.includes('bye') || msg.includes('hasta luego')) {
            return '**Hasta luego. Fue un placer ayudarte.**\n\n**Recuerda:**\n• Sigue practicando con los retos diarios\n• Explora la biblioteca para más conocimiento\n• Compite en los rankings para subir de nivel\n\nNos vemos pronto en MenTora.\n\n*Tip: Siempre puedes volver a chatear conmigo cuando necesites ayuda.*';
        }

        // Problemas técnicos
        if (msg.includes('problema') || msg.includes('error') || msg.includes('no funciona')) {
            return '**Soporte Técnico de MenTora**\n\nLamento escuchar que tienes problemas. Aquí tienes algunas soluciones:\n\n**Soluciones Rápidas:**\n• Refrescar la página (F5 o Ctrl+R)\n• Limpiar caché del navegador\n• Verificar tu conexión a internet\n• Intentar en modo incógnito\n\n**Si persiste el problema:**\n• Intenta desde otro navegador\n• Verifica que JavaScript esté habilitado\n• Desactiva extensiones que puedan interferir\n\n**Contacto Directo:**\nSi el problema continúa, contacta a nuestro equipo técnico con:\n• Descripción detallada del problema\n• Navegador y versión que usas\n• Pasos que realizaste antes del error';
        }
        
        console.log('❓ Usando respuesta default para:', msg);

        // Marcar que ya no es el primer mensaje
        if (isFirstMessage) {
            isFirstMessage = false;
        }

        // Respuesta por defecto - Solo presentación en el primer mensaje
        if (messageCount === 1) {
            // Presentación completa en el primer mensaje
            return '**Hola. Soy MenToraBot, tu asistente personal en MenTora**\n\n**Preguntas sobre la plataforma:**\n• "¿Qué es MenTora?" - Conoce nuestra plataforma educativa\n• "¿Cómo funciona?" - Gamificación y dinámicas de aprendizaje\n• "¿Es gratis?" - Información sobre acceso gratuito\n• "¿Funciona en móvil?" - Compatibilidad con dispositivos\n• "¿Cómo me registro?" - Proceso paso a paso\n• "Iniciar sesión" - Acceso a tu cuenta\n\n**Sistema de gamificación:**\n• "¿Cómo gano puntos?" - Sistema de puntuación completo\n• "Niveles" - Progresión y beneficios\n• "Insignias" - Logros y recompensas\n• "Ranking" - Competencia y posiciones\n• "Retos diarios" - Desafíos especiales\n• "Dificultad" - Niveles de retos\n\n**Gestión de cuenta:**\n• "Recuperar contraseña" - Restablecer acceso\n• "Cambiar contraseña" - Actualizar seguridad\n• "Perfil" - Personalización\n• "Notificaciones" - Configuración de alertas\n• "Mi progreso" - Estadísticas detalladas\n\n**Para profesores:**\n• "Panel de profesor" - Herramientas docentes\n• "Crear quiz" - Gestión de evaluaciones\n• "Resultados de alumnos" - Seguimiento académico\n\n**Contenido educativo:**\n• "Programación" - Python, JavaScript, algoritmos\n• "Matemáticas" - Cálculo, álgebra, estadística\n• "Biblioteca" - Recursos y materiales\n• "Categorías" - Todas las áreas disponibles\n• "Juegos" - Retos interactivos\n\n**Comunidad:**\n• "Chat" - Interacción en tiempo real\n• "Consejos de estudio" - Mejores prácticas\n• "Ayuda" - Soporte técnico\n\nEscribe cualquier tema y te daré información detallada.';
        } else {
            // Respuesta cuando no se encuentra información
            return '**Lo siento, no cuento con información sobre ese tema específico.**\n\nPuedo ayudarte con:\n• Información sobre la plataforma MenTora\n• Cómo funciona el sistema de puntos y niveles\n• Registro y acceso a la plataforma\n• Recursos de programación y matemáticas\n• Biblioteca digital y juegos\n• Panel de profesores y gestión de quizzes\n• Soporte técnico\n\n¿Hay algo más en lo que pueda asistirte?';
        }
    }

    // Función para agregar mensaje del usuario
    function addUserMessage(message) {
        const messages = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'user-message';
        messageDiv.innerHTML = `
            <div class="user-avatar">U</div>
            <div class="message-bubble user-bubble">${escapeHtml(message)}</div>
        `;
        messages.appendChild(messageDiv);
        scrollToBottom();
    }

    // Función para agregar mensaje del bot
    function addBotMessage(message) {
        const messages = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'bot-message';
        messageDiv.innerHTML = `
            <div class="bot-avatar">M</div>
            <div class="message-bubble bot-bubble">${formatBotMessage(message)}</div>
        `;
        messages.appendChild(messageDiv);
        scrollToBottom();

        // Mostrar notificación si el chat está cerrado
        if (!chatbotOpen) {
            document.getElementById('notificationDot').style.display = 'block';
        }
    }

    // Función para mostrar indicador de escritura
    function showTypingIndicator() {
        isTyping = true;
        document.getElementById('typing-indicator').style.display = 'flex';
        scrollToBottom();
    }

    // Función para ocultar indicador de escritura
    function hideTypingIndicator() {
        isTyping = false;
        document.getElementById('typing-indicator').style.display = 'none';
    }

    // Función para hacer scroll al final
    function scrollToBottom() {
        const messages = document.getElementById('chatbot-messages');
        setTimeout(() => {
            messages.scrollTop = messages.scrollHeight;
        }, 100);
    }

    // Función para escapar HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Función para formatear mensajes del bot
    function formatBotMessage(message) {
        console.log(' Formateando mensaje:', message.substring(0, 50) + '...');
        let formatted = escapeHtml(message);
        
        // Convertir markdown básico a HTML
        formatted = formatted
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **texto** -> <strong>texto</strong>
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // *texto* -> <em>texto</em>
            .replace(/\n• /g, '<br>• ') // Bullets con salto de línea
            .replace(/\n\n/g, '<br><br>') // Doble salto de línea
            .replace(/\n/g, '<br>'); // Salto de línea simple
        
        console.log('✨ Mensaje formateado completado');
        return formatted;
    }

    // Función para alternar picker de emojis (deshabilitada)
    function toggleEmojiPicker() {
        // Función deshabilitada - Sin emojis
        const input = document.getElementById('chatbot-input');
        input.focus();
    }

    // Event listeners
    document.addEventListener('DOMContentLoaded', function() {
        // Auto-focus en el input cuando se abre el chat
        const input = document.getElementById('chatbot-input');
        
        // Detectar Enter para enviar
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatbotMessage(e);
            }
        });
        
        // Prevenir envío de formulario vacío
        input.addEventListener('input', function() {
            const sendBtn = document.querySelector('.send-btn');
            sendBtn.disabled = !this.value.trim();
        });
        
        // Cerrar chat con Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && chatbotOpen) {
                toggleChatbot();
            }
        });
        
        // Mostrar notificación inicial después de unos segundos
        setTimeout(() => {
            if (!chatbotOpen) {
                document.getElementById('notificationDot').style.display = 'block';
            }
        }, 5000);
    });
