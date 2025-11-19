// =====================================================
// 🧠 MenTora Chatbot Enhanced - Base de Conocimiento Completa
// =====================================================

// Respuestas principales del bot
const botResponses = {
    'como funciona': '🎯 **MenTora - Plataforma Educativa Gamificada:**\n\n• **Quiz Interactivos:** Múltiples categorías académicas\n• **Sistema de Puntos:** Progresión de niveles 1-100\n• **Rankings:** Competencia global en tiempo real\n• **Biblioteca Digital:** 47+ recursos especializados\n• **Chat en Tiempo Real:** Comunidad de aprendizaje\n• **Panel Administrativo:** Herramientas para profesores\n\n¡Todo mientras te diviertes aprendiendo! 🚀',

    'que puedo hacer': '✨ **Funcionalidades Disponibles:**\n\n📚 **Biblioteca Digital:**\n• Programación: Python, JavaScript, Java, C++\n• Matemáticas: Cálculo, álgebra, estadística\n• Ciencias: Física, química, biología\n• Historia y literatura\n• Tecnología: IA, blockchain, cloud\n\n🎮 **Sistema de Juegos:**\n• Quiz temáticos con múltiples dificultades\n• Retos de programación ejecutables\n• Juegos colaborativos\n• Competencias por tiempo\n\n📊 **Dashboard Personal:**\n• Progreso y nivel actual\n• Estadísticas de rendimiento\n• Historial de actividades\n• Rankings y logros\n• Notificaciones importantes',

    'programacion': '💻 **Recursos de Programación:**\n\n📚 **Contenido Disponible:**\n• Python: Sintaxis, estructuras de datos, POO\n• JavaScript: ES6+, async/await, DOM\n• Java: Fundamentos, herencia, interfaces\n• C++: Punteros, templates, STL\n• HTML/CSS: Responsive design, flexbox\n• React: Componentes, hooks, contexto\n• APIs REST y Flask\n• Git y control de versiones\n• Algoritmos y estructuras de datos\n• Patrones de diseño\n• Testing y debugging\n• SQL y bases de datos\n\n🎯 **Tipos de Retos:**\n• Ejercicios de sintaxis\n• Problemas algorítmicos\n• Debugging de código\n• Optimización de rendimiento',

    'arquitectura': '🏗️ **Arquitectura Técnica MenTora:**\n\n**Backend:**\n• Flask 2.3+ con Python 3.9+\n• SQLAlchemy ORM\n• Socket.IO para WebSockets\n• Werkzeug para seguridad\n• Sistema de IA local\n\n**Base de Datos:**\n• users: Perfiles y gamificación\n• teachers: Gestión profesores\n• quizzes/questions: Evaluaciones\n• user_answers: Tracking respuestas\n• achievements/badges: Sistema logros\n• chat_messages: Comunicación\n• access_logs: Analytics\n• games: Juegos educativos\n\n**APIs Principales:**\n• /dashboard - Panel usuario\n• /admin/* - Gestión administrativa\n• /chatbot - IA conversacional\n• /games/<id>/run - Ejecución juegos',

    'gamificacion': '🎮 **Sistema de Gamificación:**\n\n**Progresión de Niveles:**\n• Niveles 1-10: 100 pts/nivel\n• Niveles 11-25: 200 pts/nivel\n• Niveles 26-50: 500 pts/nivel\n• Niveles 51-75: 1000 pts/nivel\n• Niveles 76-100: 2000 pts/nivel\n\n**Tipos de Logros:**\n• Académicos, Precisión, Sociales, Velocidad\n\n**Rankings:**\n• Global, por área, semanal y mensual',

    'biblioteca': '📚 **Biblioteca Digital:**\n\n🔍 **Categorías (47+ recursos):**\n• Programación, Matemáticas, Ciencias, Historia, Literatura, Tecnología\n\n✨ **Características:**\n• Búsqueda inteligente\n• Filtros por nivel\n• Contenido interactivo\n• Descarga offline',

    'profesores': '👨‍🏫 **Panel de Profesores:**\n\nHerramientas:\n• Crear quiz\n• Juegos educativos\n• Logros personalizables\n• Notificaciones masivas\n• Analytics avanzados\n• IA generadora de preguntas',

    'chat': '💬 **Chat en Tiempo Real:**\n\nCaracterísticas:\n• WebSockets con Socket.IO\n• Moderación IA\n• Soporte multimedia\n• Historial persistente\n• Grupos de estudio\n• Mentorías\n\nSeguridad:\n• Filtros de contenido\n• Reportes',

    'tecnico': '🔧 **Soporte Técnico:**\n\nProblemas comunes:\n• Login\n• Quiz no carga\n• Desconexión del chat\n• Rankings desactualizados\n\nOptimización recomendada:\n• Chrome/Firefox actualizados\n• JavaScript habilitado\n• 1 Mbps mínimo\n• 2GB RAM',

    'niveles': '📊 **Sistema de Niveles:**\n\nCómo ganar puntos:\n• Quiz: 10-100 pts\n• Retos: 50-200 pts\n• Actividad social: 5-25 pts\n• Biblioteca: 15-75 pts\n• Streaks: +20%\n\nLogros especiales:\n• Estudioso, Erudito, Flash, Leyenda',

    'default': '🤖 **¡Hola! Soy MenToraBot**\n\nPuedo ayudarte con programación, biblioteca, niveles, profesores, chat, arquitectura, soporte técnico y más.\n\nPregunta cosas como:\n• "¿Cómo funciona MenTora?"\n• "Programación"\n• "Gamificación"\n• "Niveles"\n• "Biblioteca"\n\n¡Estoy para ayudarte! 🚀'
};

// =====================================================
// 🎯 Patrones de intención (Regex avanzado)
// =====================================================
const intentPatterns = {
    saludo: /\b(hola|hey|saludos|buenos dias|buenas tardes|buenas noches)\b/i,
    agradecimiento: /\b(gracias|thank(s)?|thx)\b/i,
    programacion: /\b(programacion|codigo|algoritmo|python|java|javascript|desarrollo)\b/i,
    matematicas: /\b(matematicas|cálculo|calculo|algebra|estadistica|geometria)\b/i,
    tecnico: /\b(problema|error|bug|falla|crash|issue)\b/i,
    niveles: /\b(nivel(es)?|puntos|ranking|score|experiencia|xp)\b/i,
};

// =====================================================
// 🤖 FUNCIÓN INTELIGENTE PRINCIPAL
// =====================================================
function getBotResponse(message) {
    let msg = message.toLowerCase().trim();

    // 1️⃣ Búsqueda directa por clave (exacta en botResponses)
    for (const [key, response] of Object.entries(botResponses)) {
        if (key !== 'default' && msg.includes(key)) {
            return response;
        }
    }

    // 2️⃣ Coincidencia por intención (regex)
    if (intentPatterns.saludo.test(msg))
        return '👋 ¡Hola! Soy **MenToraBot**. ¿En qué puedo ayudarte hoy? 🚀';

    if (intentPatterns.agradecimiento.test(msg))
        return '¡De nada! 😊 ¿Qué más te gustaría saber sobre MenTora?';

    if (intentPatterns.programacion.test(msg))
        return botResponses.programacion;

    if (intentPatterns.matematicas.test(msg))
        return botResponses.matematicas || '🧮 Recursos matemáticos disponibles en la biblioteca.';

    if (intentPatterns.tecnico.test(msg))
        return botResponses.tecnico;

    if (intentPatterns.niveles.test(msg))
        return botResponses.niveles;

    // 3️⃣ Fallback
    return botResponses.default;
}

// =====================================================
// 🌐 Exportar para Node o navegador
// =====================================================
if (typeof module !== 'undefined') {
    module.exports = { botResponses, getBotResponse };
}
