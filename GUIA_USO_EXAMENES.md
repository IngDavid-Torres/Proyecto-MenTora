# 📚 GUÍA DE USO: Generador de Exámenes con IA Local

## 🚀 Cómo Usar el Sistema

### 1. **Acceder al Generador**
1. Inicia sesión como profesor en MenTora
2. Ve al "Panel Profesor" 
3. Busca la sección "**Generador de Exámenes con IA Local**"

### 2. **Generar Exámenes**

#### Campos a completar:
- **Tema:** Ej: "programación", "matemáticas", "historia"
- **Cantidad:** Número de preguntas (recomendado: 3-10)
- **Tipo de examen:**
  - **Solo preguntas:** Preguntas abiertas
  - **Preguntas con opciones múltiples:** A, B, C, D con respuesta correcta
- **Método de IA:**
  - **🚀 Plantillas (Rápido):** ✅ Siempre funciona, offline
  - **🦙 Ollama:** Requiere instalación separada
  - **🤗 Hugging Face:** Requiere descarga de modelos

### 3. **Temas Especializados Disponibles**

#### 💻 **Programación** (Altamente recomendado)
- Preguntas sobre Python, JavaScript, Java, C++
- Conceptos de POO, algoritmos, estructuras de datos
- Sintaxis, funciones, métodos
- Ejemplos: 
  - "¿Qué hace la función print() en Python?"
  - "¿Cuál es la diferencia entre variable y constante?"

#### 📐 **Matemáticas**
- Operaciones básicas, porcentajes
- Problemas aplicados

#### 🔬 **Ciencias**
- Química, biología, física básica

#### 📖 **Historia y Literatura**
- Eventos históricos, autores, obras

#### 🌍 **Geografía**
- Países, capitales, continentes

### 4. **Descargar Exámenes**

#### ✅ **Descarga TXT (Recomendada)**
- **Botón:** "Descargar TXT (Siempre funciona)"
- ✅ Funciona al 100%
- ✅ Incluye TODAS las preguntas generadas
- ✅ Formato legible y profesional
- ✅ Compatible con cualquier dispositivo

#### 📄 **Descarga Word**
- Requiere librería `python-docx`
- Si falla, automáticamente usa formato TXT

#### 📄 **Descarga PDF** 
- Requiere librería `reportlab`
- Si falla, automáticamente usa formato TXT

### 5. **Ejemplo de Uso Completo**

```
1. Tema: "programación"
2. Cantidad: 5
3. Tipo: "Preguntas con opciones múltiples"
4. Método: "Plantillas (Rápido)"
5. Clic en "Generar con IA Local"
6. Clic en "Descargar TXT (Siempre funciona)"
```

**Resultado esperado:**
```
EXAMEN DE INFORMATICA
==================================================
Tema: programación
Tipo: opciones
Numero de preguntas: 5
Instrucciones: Responde las siguientes preguntas.

1. ?Que hace la funcion input() en Python?
    a) Ejecuta una accion especifica
    b) Declara una variable
    c) Crea un objeto
    d) Termina el programa
    Respuesta correcta: A

2. ?Cual es la diferencia entre JavaScript y C++?
    a) Sintaxis diferente
    b) Proposito diferente
    c) Rendimiento diferente
    d) Todas las anteriores
    Respuesta correcta: A

[... más preguntas ...]
```

## 🛠 **Solución de Problemas**

### ❌ **"No se generan preguntas"**
**Solución:** 
- Usa método "Plantillas (Rápido)"
- Verifica que el tema esté en español
- Temas recomendados: "programación", "matemáticas", "ciencias"

### ❌ **"Descarga Word/PDF falla"**
**Solución:**
- Usa "Descargar TXT (Siempre funciona)"
- Para instalar librerías: `pip install python-docx reportlab`

### ❌ **"Solo se descarga 1 pregunta"**
**Solución:** 
- ✅ Ya corregido en la nueva versión
- El sistema ahora incluye TODAS las preguntas generadas
- Usa la descarga TXT para verificar

### ❌ **"Caracteres extraños (¿, ñ, acentos)"**
**Solución:**
- ✅ Ya corregido en descarga TXT
- Los caracteres se normalizan automáticamente

## 🎯 **Mejores Prácticas**

### Para Demostración:
1. **Tema:** "programación"
2. **Cantidad:** 3-5 preguntas
3. **Método:** "Plantillas (Rápido)"
4. **Descarga:** TXT

### Para Uso Productivo:
1. **Temas específicos:** "algoritmos", "bases de datos", "POO"
2. **Cantidad:** 5-10 preguntas
3. **Siempre verificar** el contenido antes de usar

## 🔍 **Verificación del Sistema**

Para verificar que todo funciona:

1. **Genera un examen de prueba:**
   - Tema: "programación"
   - Cantidad: 3
   - Tipo: opciones múltiples
   - Método: Plantillas

2. **Descarga TXT y verifica:**
   - ✅ Archivo se descarga
   - ✅ Contiene 3 preguntas
   - ✅ Cada pregunta tiene 4 opciones
   - ✅ Cada pregunta tiene respuesta correcta

## 💡 **Ventajas del Sistema**

- ✅ **100% Local:** No requiere internet
- ✅ **Sin Costos:** No usa APIs pagadas
- ✅ **Privado:** Los datos no salen del servidor
- ✅ **Confiable:** Siempre funciona con plantillas
- ✅ **Escalable:** Fácil agregar nuevos temas
- ✅ **Educativo:** Demuestra uso práctico de IA

¡Perfecto para mostrar el uso de IA en educación sin dependencias externas!