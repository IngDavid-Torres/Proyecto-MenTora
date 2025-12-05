# 🤖 Guía de Configuración del Chatbot con IA

El chatbot de MenTora puede funcionar con o sin IA:

## Opción 1: Sin IA (Modo actual - Respuestas predefinidas)
✅ **Ya está funcionando** - No requiere configuración adicional
- Responde a palabras clave específicas (python, java, variables, funciones, etc.)
- Tiene ~50 respuestas predefinidas sobre programación
- **Limitación**: Solo responde a temas predefinidos

## Opción 2: Con IA de Gemini (Recomendado - GRATIS) 🎉

### ¿Por qué usar Gemini?
- ✅ **100% GRATUITO** (hasta 60 requests por minuto)
- ✅ Responde **cualquier** pregunta de programación
- ✅ Genera ejemplos de código personalizados
- ✅ Entiende contexto y lenguaje natural
- ✅ Soporta Java, C++, Ruby, y cualquier lenguaje

### Cómo obtener tu API Key de Gemini (2 minutos):

1. **Ve a Google AI Studio**
   - Abre: https://makersuite.google.com/app/apikey
   - Inicia sesión con tu cuenta de Google

2. **Crea tu API Key**
   - Click en "Create API Key"
   - Selecciona un proyecto o crea uno nuevo
   - Copia la key generada (empieza con `AIza...`)

3. **Configura en MenTora**
   
   Opción A - Archivo `.env` (desarrollo local):
   ```bash
   # Crea o edita el archivo .env en la raíz del proyecto
   GEMINI_API_KEY=AIzaSy... # Tu key aquí
   ```

   Opción B - Variable de entorno (Railway/producción):
   ```bash
   # En Railway Dashboard > Variables
   GEMINI_API_KEY = AIzaSy... # Tu key aquí
   ```

4. **Reinicia el servidor**
   ```bash
   python app.py
   ```

5. **¡Listo!** Verás en consola:
   ```
   ✓ Gemini AI activado
   ```

### Probar el Chatbot

**Con IA activada**, prueba preguntas avanzadas:
- "¿Qué es Java y en qué se diferencia de JavaScript?"
- "Explícame los design patterns en programación"
- "¿Cómo hacer una API REST en Python?"
- "Dame un ejemplo de recursión en C++"

**Sin IA** (solo respuestas predefinidas):
- "python" → Respuesta básica
- "java" → Respuesta básica
- Preguntas avanzadas → Mensaje por defecto

### Límites de Gemini (Plan gratuito)
- 60 requests por minuto
- 1500 requests por día
- Más que suficiente para una plataforma educativa

### ¿Problemas?

**"Gemini no responde"**
- Verifica que la API key esté correcta
- Revisa la consola del servidor para errores
- El chatbot automáticamente usará respuestas predefinidas como fallback

**"Quiero usar OpenAI en vez de Gemini"**
- Gemini es gratuito y muy bueno para educación
- OpenAI GPT-4 es de pago (~$0.03 por 1K tokens)
- Si insistes, agrega `OPENAI_API_KEY` en `.env`

### Seguridad

⚠️ **IMPORTANTE**:
- Nunca subas tu `.env` a Git (ya está en `.gitignore`)
- No compartas tu API key públicamente
- Si la expones accidentalmente, revócala y crea una nueva

---

## Comparación de Modos

| Característica | Sin IA | Con Gemini IA |
|---------------|--------|---------------|
| Costo | Gratis | Gratis |
| Setup | 0 min | 2 min |
| Preguntas | ~50 predefinidas | Ilimitadas |
| Calidad | Básica | Avanzada |
| Lenguajes | Python, JS, Java | Todos |
| Ejemplos código | Estáticos | Personalizados |
| Contexto | No entiende | Sí entiende |

## Conclusión

Para una experiencia educativa completa, **configura Gemini** (es gratis y toma 2 minutos). Si prefieres simplicidad, el modo sin IA ya funciona para temas básicos.

¿Preguntas? Abre un issue en GitHub o consulta la documentación de Gemini: https://ai.google.dev/docs
