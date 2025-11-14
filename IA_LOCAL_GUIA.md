# 🤖 Guía de IA Local para MenTora

## 📋 Opciones Disponibles

### 1. 🚀 **Plantillas (Recomendado para demostración)**
- ✅ **Ya funciona** - No requiere instalación adicional
- ✅ Rápido y confiable
- ✅ Ideal para demostrar funcionalidad
- ✅ Funciona completamente offline

### 2. 🦙 **Ollama (IA Avanzada)**
- Modelos locales de alta calidad
- Requiere instalación de Ollama

#### Instalación de Ollama:
```bash
# 1. Descargar e instalar Ollama desde https://ollama.ai
# 2. Instalar un modelo (elige uno):

# Modelo pequeño y rápido (recomendado):
ollama pull llama3.2:1b

# Modelo mediano (mejor calidad):
ollama pull llama3.2:3b

# Modelo completo (máxima calidad, requiere más RAM):
ollama pull llama3.2

# Alternativa - Mistral (muy bueno para español):
ollama pull mistral
```

#### Verificar instalación:
```bash
# Verificar que Ollama esté corriendo:
curl http://localhost:11434/api/tags
```

### 3. 🤗 **Hugging Face Transformers**
- Modelos preentrenados
- Descarga automática la primera vez

#### Instalación:
```bash
pip install transformers torch
```

## 🔧 Configuración en MenTora

### Método 1: Usar Plantillas (Sin instalación)
1. Selecciona "🚀 Plantillas (Rápido)" en el generador
2. ¡Ya funciona! Genera preguntas inteligentes basadas en plantillas

### Método 2: Configurar Ollama
1. Instala Ollama y un modelo (ver arriba)
2. Asegúrate de que Ollama esté corriendo
3. Selecciona "🦙 Ollama" en el generador
4. Si falla, automáticamente usa plantillas como respaldo

### Método 3: Configurar Hugging Face
1. Instala las dependencias: `pip install transformers torch`
2. Selecciona "🤗 Hugging Face" en el generador
3. La primera vez descargará el modelo automáticamente

## 🎯 Ejemplos de Uso

### Matemáticas:
```
Tema: "álgebra básica"
Resultado: "¿Cuál es el resultado de 15 + 23?"
Opciones: [38, 35, 40, 42]
Respuesta: A
```

### Ciencias:
```
Tema: "biología"  
Resultado: "¿Cuál es la función principal del corazón en el cuerpo humano?"
```

### Historia:
```
Tema: "independencia de méxico"
Resultado: "¿En qué año ocurrió la Independencia de México?"
```

## 🚨 Solución de Problemas

### Si Ollama no funciona:
1. Verifica que esté instalado: `ollama --version`
2. Verifica que esté corriendo: `ollama serve`
3. Prueba descargar un modelo: `ollama pull llama3.2:1b`

### Si Hugging Face da error:
1. Instala dependencias: `pip install transformers torch`
2. Verifica espacio en disco (los modelos pueden ser grandes)
3. En la primera ejecución puede tardar en descargar

### Si todo falla:
- **¡No hay problema!** El sistema siempre usa plantillas como respaldo
- Las plantillas generan preguntas inteligentes sin necesidad de IA externa

## 💡 Recomendaciones

### Para Demostración:
- **Usa Plantillas**: Rápido, confiable, ya funciona

### Para Producción:
- **Usa Ollama**: Mejor calidad, completamente local, sin costos

### Para Desarrollo:
- **Usa Hugging Face**: Buena calidad, fácil de configurar

## 🔍 Verificar que Todo Funciona

```bash
# Ejecutar el test del generador:
cd /ruta/a/MenTora
python ai_local.py
```

Deberías ver preguntas generadas exitosamente.

## 📊 Comparación de Métodos

| Método | Velocidad | Calidad | Instalación | Tamaño |
|--------|-----------|---------|-------------|---------|
| Plantillas | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Ya funciona | 0 MB |
| Ollama | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Manual | 500MB - 4GB |
| Hugging Face | ⭐⭐ | ⭐⭐⭐⭐ | Automática | 200MB - 1GB |

## 🎓 Para Profesores

La implementación de IA local en MenTora demuestra:

1. **Independencia tecnológica**: No dependemos de servicios externos
2. **Privacidad**: Los datos nunca salen del servidor local
3. **Costos**: Sin gastos en APIs externas
4. **Flexibilidad**: Múltiples métodos según las necesidades
5. **Robustez**: Sistema de respaldo automático

¡Perfecto para mostrar el uso práctico de IA en educación!