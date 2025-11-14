// MenTora Chatbot Enhanced - Base de conocimientos completa
const botResponses = {
    'como funciona': '🎯 **MenTora - Plataforma Educativa Gamificada:**\n\n• **Quiz Interactivos:** Múltiples categorías académicas\n• **Sistema de Puntos:** Progresión de niveles 1-100\n• **Rankings:** Competencia global en tiempo real\n• **Biblioteca Digital:** 47+ recursos especializados\n• **Chat en Tiempo Real:** Comunidad de aprendizaje\n• **Panel Administrativo:** Herramientas para profesores\n\n¡Todo mientras te diviertes aprendiendo! 🚀',
    
    'que puedo hacer': '✨ **Funcionalidades Disponibles:**\n\n📚 **Biblioteca Digital:**\n• Programación: Python, JavaScript, Java, C++\n• Matemáticas: Cálculo, álgebra, estadística\n• Ciencias: Física, química, biología\n• Historia y literatura\n• Tecnología: IA, blockchain, cloud\n\n🎮 **Sistema de Juegos:**\n• Quiz temáticos con múltiples dificultades\n• Retos de programación ejecutables\n• Juegos colaborativos\n• Competencias por tiempo\n\n📊 **Dashboard Personal:**\n• Progreso y nivel actual\n• Estadísticas de rendimiento\n• Historial de actividades\n• Rankings y logros\n• Notificaciones importantes',
    
    'programacion': '💻 **Recursos de Programación:**\n\n📚 **Contenido Disponible:**\n• Python: Sintaxis, estructuras de datos, POO\n• JavaScript: ES6+, async/await, DOM\n• Java: Fundamentos, herencia, interfaces\n• C++: Punteros, templates, STL\n• HTML/CSS: Responsive design, flexbox\n• React: Componentes, hooks, contexto\n• APIs REST y Flask\n• Git y control de versiones\n• Algoritmos y estructuras de datos\n• Patrones de diseño\n• Testing y debugging\n• SQL y bases de datos\n\n🎯 **Tipos de Retos:**\n• Ejercicios de sintaxis\n• Problemas algorítmicos\n• Debugging de código\n• Optimización de rendimiento',
    
    'arquitectura': '🏗️ **Arquitectura Técnica MenTora:**\n\n**Backend:**\n• Flask 2.3+ con Python 3.9+\n• SQLAlchemy ORM\n• Socket.IO para WebSockets\n• Werkzeug para seguridad\n• Sistema de IA local\n\n**Base de Datos:**\n• users: Perfiles y gamificación\n• teachers: Gestión profesores\n• quizzes/questions: Evaluaciones\n• user_answers: Tracking respuestas\n• achievements/badges: Sistema logros\n• chat_messages: Comunicación\n• access_logs: Analytics\n• games: Juegos educativos\n\n**APIs Principales:**\n• /dashboard - Panel usuario\n• /admin/* - Gestión administrativa\n• /chatbot - IA conversacional\n• /games/<id>/run - Ejecución juegos',
    
    'gamificacion': '🎮 **Sistema de Gamificación:**\n\n**Progresión de Niveles:**\n• Niveles 1-10: 100 pts/nivel (Principiante)\n• Niveles 11-25: 200 pts/nivel (Intermedio)\n• Niveles 26-50: 500 pts/nivel (Avanzado)\n• Niveles 51-75: 1000 pts/nivel (Experto)\n• Niveles 76-100: 2000 pts/nivel (Maestro)\n\n**Tipos de Logros:**\n• Académicos: Perfeccionista, Estudioso\n• Velocidad: Flash, Supersónico\n• Precisión: Certero, Infalible\n• Sociales: Mentor, Colaborador\n• Progresión: Imparable, Dedicado\n\n**Rankings:**\n• Global por puntos totales\n• Por áreas académicas\n• Semanal y mensual\n• Solo estudiantes',
    
    'biblioteca': '📚 **Biblioteca Digital:**\n\n🔍 **Categorías (47+ recursos):**\n• **Programación (12):** Lenguajes, algoritmos, frameworks\n• **Matemáticas (8):** Álgebra, cálculo, estadística\n• **Ciencias (6):** Física, química, biología\n• **Historia (5):** Universal, México, contemporánea\n• **Literatura (7):** Clásica, análisis, escritura\n• **Tecnología (9):** IA, blockchain, cloud, IoT\n\n✨ **Características:**\n• Búsqueda inteligente\n• Filtros por nivel\n• Contenido interactivo\n• Descarga offline\n• Progreso automático',
    
    'profesores': '👨‍🏫 **Panel de Profesores:**\n\n🛠️ **Herramientas Disponibles:**\n• Crear quiz personalizados\n• Desarrollar juegos educativos\n• Sistema de logros personalizable\n• Envío de notificaciones masivas\n• Estadísticas detalladas estudiantes\n• Generación automática con IA\n• Gestión de usuarios\n• Analytics institucional\n• Reportes exportables\n\n📊 **Funciones de IA:**\n• Generación automática de preguntas\n• Análisis de dificultad\n• Personalización por nivel\n• Exportación múltiples formatos',
    
    'chat': '💬 **Chat en Tiempo Real:**\n\n🌐 **Características Técnicas:**\n• WebSockets con Socket.IO\n• Moderación automática IA\n• Soporte multimedia\n• Emojis y reacciones\n• Historial persistente\n\n💡 **Usos Educativos:**\n• Resolver dudas académicas\n• Formar grupos de estudio\n• Celebrar logros\n• Debates constructivos\n• Mentorías entre usuarios\n\n🛡️ **Moderación:**\n• Filtros de contenido\n• Sistema de reportes\n• Ambiente de aprendizaje seguro',
    
    'tecnico': '🔧 **Soporte Técnico:**\n\n**Problemas Comunes:**\n• Login: Verificar credenciales, limpiar cache\n• Quiz no carga: Refresh, verificar conexión\n• Chat desconectado: Reconexión automática\n• Rankings: Cache temporal, esperar 5-10 min\n\n**Optimización:**\n• Chrome 90+ o Firefox 88+ recomendados\n• JavaScript habilitado\n• Conexión estable 1Mbps mínimo\n• 2GB RAM disponible\n\n**Contacto:**\n• Chat técnico 24/7\n• Documentación en /help',
    
    'niveles': '📊 **Sistema de Niveles:**\n\n🎯 **Cómo Ganar Puntos:**\n• Quiz completados: 10-100 pts\n• Retos diarios: 50-200 pts bonus\n• Actividad social: 5-25 pts\n• Uso biblioteca: 15-75 pts\n• Streaks consecutivos: +20% acumulativo\n\n📈 **Progresión:**\n• 100 niveles totales\n• Escala exponencial balanceada\n• Beneficios progresivos\n• Reconocimientos especiales\n\n🏆 **Logros Especiales:**\n• Primer Paso, Estudioso, Erudito\n• Velocista, Rayo, Flash\n• Certero, Perfeccionista, Leyenda\n• Comunicador, Mentor, Líder',
    
    'default': '🤖 **¡Hola! Soy MenToraBot**\n\nSoy el asistente oficial de MenTora con conocimiento completo de la plataforma.\n\n**Puedo ayudarte con:**\n• Arquitectura técnica (Flask, SQLAlchemy, WebSockets)\n• Funcionalidades educativas completas\n• Sistema de gamificación y niveles\n• Herramientas para profesores\n• Resolución de problemas\n• Estrategias de estudio\n\n**Pregúntame sobre:**\n• "¿Cómo funciona MenTora?"\n• "¿Qué puedo hacer aquí?"\n• "Programación", "Matemáticas", "Biblioteca"\n• "Niveles", "Gamificación", "Chat"\n• "Profesores", "Arquitectura", "Soporte técnico"\n\n¡Estoy aquí para hacer tu experiencia en MenTora increíble! 🚀'
};

// Función mejorada para obtener respuestas
function getBotResponse(message) {
    const msg = message.toLowerCase().trim();
    
    // Búsqueda exacta por palabras clave
    for (const [key, response] of Object.entries(botResponses)) {
        if (key !== 'default' && msg.includes(key.replace(/\s+/g, ' '))) {
            return response;
        }
    }
    
    // Patrones específicos
    if (msg.match(/(hola|hey|saludos|buenos|buenas)/)) {
        return '👋 ¡Hola! Soy **MenToraBot**, tu asistente especializado. ¿En qué puedo ayudarte con MenTora? 🚀';
    }
    
    if (msg.match(/(gracias|thank|thx)/)) {
        return '¡De nada! 😊 ¿Hay algo más sobre MenTora que quieras saber?';
    }
    
    if (msg.match(/(programacion|codigo|algoritmo|python|java|javascript)/)) {
        return botResponses.programacion;
    }
    
    if (msg.match(/(matematicas|calculo|algebra|estadistica)/)) {
        return botResponses.matematicas || '🧮 **Matemáticas:** Recursos de cálculo, álgebra, estadística y más disponibles en la biblioteca.';
    }
    
    if (msg.match(/(problema|error|bug|falla)/)) {
        return botResponses.tecnico;
    }
    
    if (msg.match(/(nivel|puntos|ranking|score)/)) {
        return botResponses.niveles;
    }
    
    // Respuesta por defecto
    return botResponses.default;
}

// Exportar para uso en el HTML
if (typeof module !== 'undefined') {
    module.exports = { botResponses, getBotResponse };
}