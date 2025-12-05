"""
Servicio de IA para MenToraBot
Soporta Google Gemini API y fallback a respuestas predefinidas
"""
import os
from config import GEMINI_API_KEY

# Importar Gemini solo si está disponible
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

class AIService:
    def __init__(self):
        self.use_ai = False
        self.model = None
        
        # Configurar Gemini si hay API key y la librería está disponible
        if GEMINI_AVAILABLE and GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
                self.use_ai = True
                print("✓ Gemini AI activado")
            except Exception as e:
                print(f"⚠ Error al configurar Gemini: {e}")
                self.use_ai = False
        elif not GEMINI_AVAILABLE:
            print("⚠ google-generativeai no instalado - usando respuestas predefinidas")
        else:
            print("⚠ GEMINI_API_KEY no configurada - usando respuestas predefinidas")
    
    def get_response(self, user_message):
        """
        Obtiene respuesta usando IA o respuestas predefinidas
        """
        if not user_message or not user_message.strip():
            return "Por favor, escribe tu pregunta sobre programación."
        
        # Si tenemos IA disponible, usarla
        if self.use_ai and self.model:
            try:
                return self._get_ai_response(user_message)
            except Exception as e:
                print(f"Error en IA: {e}")
                # Fallback a respuestas predefinidas
                return self._get_fallback_response(user_message)
        else:
            # Usar respuestas predefinidas
            return self._get_fallback_response(user_message)
    
    def _get_ai_response(self, user_message):
        """
        Obtiene respuesta de Gemini AI
        """
        # Prompt del sistema para MenToraBot
        system_prompt = """Eres MenToraBot, un asistente de programación amigable y educativo.
Tu misión es ayudar a estudiantes a aprender programación.

INSTRUCCIONES:
- Responde en español
- Sé conciso pero completo (máximo 200 palabras)
- Usa ejemplos de código cuando sea apropiado
- Si mencionas código, usa formato markdown
- Enfócate en explicar conceptos de forma clara
- Temas principales: Python, JavaScript, Java, C++, HTML/CSS, estructuras de datos, algoritmos, POO, bases de datos, Git
- Si te preguntan sobre un tema fuera de programación, redirige amablemente al tema educativo
"""
        
        full_prompt = f"{system_prompt}\n\nPregunta del estudiante: {user_message}\n\nRespuesta:"
        
        response = self.model.generate_content(full_prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Lo siento, no pude generar una respuesta. ¿Podrías reformular tu pregunta?"
    
    def _get_fallback_response(self, user_message):
        """
        Respuestas predefinidas cuando no hay IA disponible
        """
        msg = user_message.lower().strip()
        
        # Diccionario de respuestas predefinidas
        responses = {
            # Saludos
            'hola': '¡Hola! 👋 Soy MenToraBot. Estoy aquí para ayudarte con tus preguntas sobre programación. ¿Qué te gustaría aprender?',
            'buenos dias': '¡Buenos días! ¿En qué tema de programación puedo ayudarte hoy?',
            'buenas tardes': '¡Buenas tardes! ¿Tienes alguna pregunta sobre programación?',
            
            # Python
            'python': 'Python es un lenguaje interpretado de alto nivel. Características:\n• Sintaxis clara y legible\n• Multiparadigma (POO, funcional, imperativo)\n• Gran ecosistema de librerías\n• Usado en web, IA, data science, automatización\n\nEjemplo básico:\n```python\ndef saludar(nombre):\n    return f"Hola {nombre}"\n\nprint(saludar("Ana"))\n```',
            
            'variable': 'Las variables almacenan datos en memoria. En Python:\n```python\nnombre = "Juan"  # String\nedad = 25        # Integer\naltura = 1.75    # Float\nes_estudiante = True  # Boolean\n```\n\nBuenas prácticas:\n• Nombres descriptivos\n• snake_case en Python\n• Evitar palabras reservadas',
            
            'funcion': 'Las funciones son bloques de código reutilizables:\n```python\ndef calcular_area(base, altura):\n    """Calcula el área de un rectángulo"""\n    return base * altura\n\nresultado = calcular_area(5, 3)\nprint(resultado)  # 15\n```\n\nVentajas: reutilización, organización, testing.',
            
            'lista': 'Las listas son colecciones ordenadas y mutables:\n```python\nfrutas = ["manzana", "banana", "naranja"]\nfrutas.append("uva")  # Agregar\nfrutas[0]  # Acceder: "manzana"\nfrutas.remove("banana")  # Eliminar\n```\n\nMétodos útiles: append(), insert(), pop(), sort(), reverse()',
            
            # JavaScript
            'javascript': 'JavaScript es el lenguaje de la web. Usos:\n• Frontend (manipular DOM)\n• Backend (Node.js)\n• Apps móviles (React Native)\n• Apps desktop (Electron)\n\nEjemplo ES6:\n```javascript\nconst saludar = (nombre) => {\n    return `Hola ${nombre}`;\n};\n\nconsole.log(saludar("María"));\n```',
            
            'java': 'Java es un lenguaje orientado a objetos, compilado y multiplataforma.\n\nCaracterísticas:\n• Write Once, Run Anywhere (JVM)\n• Fuertemente tipado\n• Gran ecosistema empresarial\n• Usado en Android, backend, sistemas\n\nEjemplo:\n```java\npublic class HolaMundo {\n    public static void main(String[] args) {\n        System.out.println("Hola Mundo");\n    }\n}\n```',
            
            # Conceptos generales
            'programacion': 'La programación es el proceso de crear instrucciones para que una computadora resuelva problemas.\n\nConceptos clave:\n• Variables y tipos de datos\n• Estructuras de control (if, loops)\n• Funciones y modularidad\n• Estructuras de datos\n• Algoritmos\n• POO (Programación Orientada a Objetos)\n\n¿Sobre qué concepto específico quieres aprender?',
            
            'algoritmo': 'Un algoritmo es una secuencia de pasos para resolver un problema.\n\nCaracterísticas:\n• Finito (termina)\n• Definido (pasos claros)\n• Entrada y salida\n• Efectivo (ejecutable)\n\nEjemplo - Búsqueda lineal:\n```python\ndef buscar(lista, valor):\n    for i, elemento in enumerate(lista):\n        if elemento == valor:\n            return i\n    return -1\n```',
            
            'poo': 'POO (Programación Orientada a Objetos) organiza código en objetos.\n\nPilares:\n• Encapsulamiento\n• Herencia\n• Polimorfismo\n• Abstracción\n\nEjemplo en Python:\n```python\nclass Persona:\n    def __init__(self, nombre, edad):\n        self.nombre = nombre\n        self.edad = edad\n    \n    def saludar(self):\n        return f"Hola, soy {self.nombre}"\n\np = Persona("Ana", 25)\nprint(p.saludar())\n```',
            
            'clase': 'Una clase es una plantilla para crear objetos:\n```python\nclass Rectangulo:\n    def __init__(self, base, altura):\n        self.base = base\n        self.altura = altura\n    \n    def area(self):\n        return self.base * self.altura\n\nrect = Rectangulo(5, 3)\nprint(rect.area())  # 15\n```',
            
            # Bases de datos
            'sql': 'SQL (Structured Query Language) gestiona bases de datos relacionales.\n\nOperaciones CRUD:\n```sql\n-- CREATE\nINSERT INTO usuarios (nombre, email) VALUES ("Ana", "ana@mail.com");\n\n-- READ\nSELECT * FROM usuarios WHERE edad > 18;\n\n-- UPDATE\nUPDATE usuarios SET email = "nuevo@mail.com" WHERE id = 1;\n\n-- DELETE\nDELETE FROM usuarios WHERE id = 5;\n```',
            
            'base de datos': 'Las bases de datos almacenan información de forma organizada.\n\nTipos:\n• Relacionales (SQL): MySQL, PostgreSQL\n• NoSQL: MongoDB, Firebase\n• En memoria: Redis\n\n¿Quieres saber sobre SQL específicamente?',
            
            # Git
            'git': 'Git es un sistema de control de versiones.\n\nComandos básicos:\n```bash\ngit init              # Iniciar repo\ngit add .             # Agregar cambios\ngit commit -m "msg"   # Guardar cambios\ngit push              # Subir a remoto\ngit pull              # Descargar cambios\ngit branch            # Ver ramas\ngit checkout -b rama  # Crear rama\n```',
            
            # HTML/CSS
            'html': 'HTML estructura el contenido web:\n```html\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Mi Página</title>\n</head>\n<body>\n    <h1>Bienvenido</h1>\n    <p>Este es un párrafo</p>\n    <a href="pagina.html">Enlace</a>\n</body>\n</html>\n```\n\nEtiquetas comunes: div, p, h1-h6, img, a, ul/ol, form',
            
            'css': 'CSS estiliza páginas web:\n```css\n.contenedor {\n    display: flex;\n    justify-content: center;\n    background-color: #f0f0f0;\n    padding: 20px;\n}\n\n.titulo {\n    color: #333;\n    font-size: 24px;\n    font-weight: bold;\n}\n```\n\nConceptos: selectores, box model, flexbox, grid',
        }
        
        # Buscar coincidencias en el mensaje
        for keyword, response in responses.items():
            if keyword in msg:
                return response
        
        # Respuesta por defecto
        return """Como asistente de programación, puedo ayudarte con:

• **Lenguajes**: Python, JavaScript, Java, C++, HTML/CSS
• **Conceptos**: Variables, funciones, clases, POO
• **Estructuras**: Listas, diccionarios, arrays, algoritmos
• **Herramientas**: Git, bases de datos SQL
• **Web**: HTML, CSS, JavaScript, APIs

¿Sobre qué tema específico te gustaría aprender? Por ejemplo: "¿Qué es Python?", "Explica las funciones", "¿Cómo usar Git?"

💡 **Tip**: Para obtener respuestas más avanzadas, el administrador puede configurar la API de Gemini."""

# Instancia global del servicio
ai_service = AIService()
