# Funciones auxiliares para descargas de exámenes
import json
from io import BytesIO

def create_text_exam(tema, area, tipo_examen, preguntas):
    """Crea un examen en formato texto plano"""
    content = f"EXAMEN DE {area.upper()}\n"
    content += "=" * 50 + "\n"
    content += f"Tema: {tema}\n"
    content += f"Tipo: {tipo_examen}\n"
    content += f"Numero de preguntas: {len(preguntas)}\n"
    content += "Instrucciones: Responde las siguientes preguntas.\n\n"
    
    if tipo_examen == 'opciones' and preguntas and isinstance(preguntas[0], dict):
        for i, q in enumerate(preguntas, 1):
            # Obtener pregunta y limpiar caracteres problemáticos
            pregunta_text = q.get('pregunta', f'Pregunta {i}')
            pregunta_text = pregunta_text.replace('¿', '?').replace('¡', '!').replace('ñ', 'n')
            pregunta_text = pregunta_text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            
            content += f"{i}. {pregunta_text}\n"
            
            opciones = q.get('opciones', [])
            for idx, opt in enumerate(opciones):
                # Limpiar opciones también
                opt_clean = str(opt).replace('¿', '?').replace('¡', '!').replace('ñ', 'n')
                opt_clean = opt_clean.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                content += f"    {chr(97+idx)}) {opt_clean}\n"
            
            respuesta = q.get('respuesta', '')
            if respuesta:
                content += f"    Respuesta correcta: {respuesta}\n"
            content += "\n"
    else:
        for i, q in enumerate(preguntas, 1):
            if isinstance(q, dict):
                pregunta_text = q.get('pregunta', str(q))
            else:
                pregunta_text = str(q)
                
            # Limpiar caracteres problemáticos
            pregunta_text = pregunta_text.replace('¿', '?').replace('¡', '!').replace('ñ', 'n')
            pregunta_text = pregunta_text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            
            content += f"{i}. {pregunta_text}\n\n"
    
    content += "\n" + "=" * 50 + "\n"
    content += f"Examen generado por MenTora - IA Local\n"
    content += f"Total de preguntas procesadas: {len(preguntas)}\n"
    content += f"Metodo de generacion: Sistema de plantillas offline\n"
    
    return content

def debug_preguntas_info(preguntas_raw):
    """Función para debuggear problemas con las preguntas"""
    info = {
        'raw_length': len(preguntas_raw),
        'raw_preview': preguntas_raw[:300],
        'json_valid': False,
        'parsed_count': 0,
        'error': None
    }
    
    try:
        parsed = json.loads(preguntas_raw)
        info['json_valid'] = True
        info['parsed_count'] = len(parsed) if isinstance(parsed, list) else 1
        info['first_item'] = parsed[0] if parsed and isinstance(parsed, list) else parsed
    except Exception as e:
        info['error'] = str(e)
    
    return info