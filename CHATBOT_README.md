# 🎓 MenToraBot - Sistema de Chatbot Inteligente

## ✅ Estado Actual

El chatbot **YA ESTÁ FUNCIONANDO** con respuestas mejoradas de programación. Ahora puede responder a preguntas sobre:

### Temas Disponibles (Respuestas Predefinidas):
- **Lenguajes**: Python, JavaScript, Java, HTML, CSS
- **Conceptos básicos**: Variables, funciones, clases, listas, diccionarios
- **Programación orientada a objetos**: Herencia, polimorfismo, encapsulamiento
- **Estructuras de datos**: Arrays, algoritmos, recursión
- **Desarrollo web**: React, APIs, bases de datos SQL
- **Herramientas**: Git, debugging, clean code

### Ejemplo de conversación:
```
Usuario: "hola"
Bot: "¡Hola! 👋 Soy MenToraBot. Puedo ayudarte con Python, JavaScript, HTML/CSS..."

Usuario: "que es python"
Bot: "Python es un lenguaje interpretado de alto nivel. Características:
• Sintaxis clara y legible
• Multiparadigma (POO, funcional, imperativo)
• Gran ecosistema de librerías..."

Usuario: "explica funciones"
Bot: "Las funciones son bloques de código reutilizables:
```python
def calcular_area(base, altura):
    return base * altura
```
Ventajas: reutilización, organización, testing."
```

---

## 🚀 Upgrade a IA Avanzada (Opcional)

Para habilitar respuestas a **CUALQUIER** pregunta de programación (no solo las predefinidas), puedes activar la integración con **Google Gemini AI** (es gratuita).

### Beneficios de activar Gemini:
- ✅ Responde preguntas sobre **cualquier** lenguaje (Ruby, Rust, Go, C#, etc.)
- ✅ Genera ejemplos de código personalizados según el contexto
- ✅ Entiende preguntas complejas en lenguaje natural
- ✅ Explica conceptos avanzados (design patterns, arquitecturas, etc.)
- ✅ **100% GRATIS** (hasta 60 requests/minuto)

### Cómo activar Gemini (2 minutos):

1. **Obtén tu API Key gratuita**:
   - Ve a: https://makersuite.google.com/app/apikey
   - Inicia sesión con Google
   - Click en "Create API Key"
   - Copia la key generada

2. **Configura la variable de entorno**:
   
   **Opción A - Desarrollo local** (archivo `.env`):
   ```bash
   # Crea o edita .env en la raíz del proyecto
   GEMINI_API_KEY=AIzaSy...tu-key-aqui
   ```

   **Opción B - Railway/Producción**:
   ```
   Variables de entorno en Railway:
   GEMINI_API_KEY = AIzaSy...tu-key-aqui
   ```

3. **Reinicia el servidor**:
   ```bash
   python app.py
   ```

4. **Verifica la activación** en la consola:
   ```
   ✓ Gemini AI activado
    MenTora está en línea
   ```

5. **¡Prueba el chatbot!**
   ```
   Usuario: "explícame el patrón Singleton en Java con ejemplo"
   Bot: [Respuesta completa y personalizada generada por IA]
   ```

---

## 📋 Comparación de Modos

| Característica | Sin IA (Actual) | Con Gemini IA |
|----------------|-----------------|---------------|
| **Estado** | ✅ Activado | ⚙️ Requiere configuración |
| **Costo** | Gratis | Gratis |
| **Setup** | Ya funciona | 2 minutos |
| **Respuestas** | ~50 temas predefinidos | Ilimitadas |
| **Lenguajes** | Python, JS, Java | Todos (Rust, Go, C++, etc) |
| **Flexibilidad** | Palabras clave exactas | Lenguaje natural |
| **Código** | Ejemplos estáticos | Ejemplos personalizados |
| **Temas** | Básicos/intermedios | Básicos + avanzados |

---

## 🛠️ Arquitectura Técnica

### Sin IA (Modo actual):
```
Usuario → Frontend → /chatbot → ai_service.py 
                                    ↓
                          _get_fallback_response()
                                    ↓
                            Respuestas predefinidas
```

### Con IA activada:
```
Usuario → Frontend → /chatbot → ai_service.py
                                    ↓
                          _get_ai_response()
                                    ↓
                          Google Gemini API
                                    ↓
                          Respuesta generada con IA
```

### Archivos modificados:
- ✅ `app.py` - Endpoint del chatbot simplificado
- ✅ `ai_service.py` - **NUEVO** - Servicio de IA con fallback
- ✅ `config.py` - Variables de configuración para API keys
- ✅ `requirements.txt` - Agregado `google-generativeai`
- ✅ `script_usser.js` - Mensaje de bienvenida automático

---

## 🧪 Probar el Chatbot

### Tests básicos (funcionan ahora):
```
1. "hola" → Saludo personalizado
2. "que es python" → Explicación de Python
3. "explica funciones" → Concepto con ejemplo
4. "que es POO" → Pilares de programación orientada a objetos
5. "git" → Comandos básicos de Git
```

### Tests avanzados (requieren Gemini IA):
```
1. "explica el patrón Observer en C++"
2. "diferencias entre async/await y callbacks en Node.js"
3. "cómo implementar un árbol binario en Rust"
4. "mejores prácticas de seguridad en APIs REST"
```

---

## ❓ FAQ

**P: ¿El chatbot funciona sin configurar nada?**
R: Sí, actualmente responde a ~50 temas de programación con respuestas predefinidas.

**P: ¿Por qué activar Gemini si ya funciona?**
R: Para responder **cualquier** pregunta, no solo las 50 predefinidas. Gemini entiende contexto y genera código personalizado.

**P: ¿Gemini es realmente gratis?**
R: Sí, hasta 60 requests/minuto. Más que suficiente para una plataforma educativa.

**P: ¿Qué pasa si no configuro Gemini?**
R: El chatbot usa automáticamente las respuestas predefinidas (modo actual).

**P: ¿Puedo usar OpenAI en vez de Gemini?**
R: Sí, pero es de pago. Gemini es gratuito y muy bueno para educación.

**P: ¿La API key es segura?**
R: Sí, el archivo `.env` está en `.gitignore`. Nunca se sube a Git.

---

## 📚 Recursos

- [Documentación de Gemini](https://ai.google.dev/docs)
- [Obtener API Key](https://makersuite.google.com/app/apikey)
- [Guía completa de configuración](./CHATBOT_IA_SETUP.md)

---

## 🎯 Próximos Pasos

1. ✅ **Chatbot funcionando** con respuestas predefinidas
2. ⚙️ **Opcional**: Activar Gemini para respuestas avanzadas
3. 💡 **Futuro**: Agregar historial de conversación
4. 🚀 **Futuro**: Sugerencias de ejercicios personalizados

---

¿Preguntas? Revisa `CHATBOT_IA_SETUP.md` para más detalles.
