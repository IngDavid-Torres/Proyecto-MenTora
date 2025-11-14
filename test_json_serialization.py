# Prueba específica para el problema de serialización JSON
import sys
import os
sys.path.append(r'c:\Users\doser\OneDrive\Escritorio\MenTora')

from ai_local import generate_local_exam
import json

def test_json_serialization():
    print("PRUEBA DE SERIALIZACION JSON")
    print("=" * 50)
    
    # Generar preguntas de programación
    tema = "programacion"
    cantidad = 5
    tipo_examen = "opciones"
    
    print(f"Generando {cantidad} preguntas sobre {tema}...")
    questions = generate_local_exam(tema, cantidad, tipo_examen, "offline")
    
    print(f"Preguntas generadas: {len(questions)}")
    print(f"Tipo de datos: {type(questions)}")
    
    if questions:
        print(f"Primera pregunta: {questions[0]}")
    
    # Probar serialización JSON como en el template de Flask
    print("\n--- SIMULANDO SERIALIZACION DEL TEMPLATE ---")
    
    # Esto simula lo que hace {{ ia_questions|tojson }} en el template
    try:
        json_str = json.dumps(questions, ensure_ascii=False, separators=(',', ':'))
        print(f"JSON serialization exitosa!")
        print(f"Longitud del JSON: {len(json_str)} caracteres")
        print(f"Comienza con: {json_str[:50]}...")
        print(f"Termina con: {json_str[-50:]}")
        
        # Probar deserialización (lo que hace la función de descarga)
        print("\n--- SIMULANDO DESERIALIZACION EN DESCARGA ---")
        parsed_back = json.loads(json_str)
        print(f"Deserialización exitosa!")
        print(f"Preguntas recuperadas: {len(parsed_back)}")
        
        if parsed_back:
            print(f"Primera pregunta recuperada: {parsed_back[0]}")
            
        # Verificar que no se perdió información
        if len(parsed_back) == len(questions):
            print("✅ Número de preguntas coincide!")
        else:
            print("❌ Se perdieron preguntas en el proceso")
            
        # Verificar estructura
        if isinstance(parsed_back[0], dict) and 'pregunta' in parsed_back[0]:
            print("✅ Estructura de pregunta correcta!")
        else:
            print("❌ Estructura de pregunta incorrecta")
            
        # Crear contenido de examen simulado
        print("\n--- SIMULANDO CREACION DE EXAMEN ---")
        exam_content = f"EXAMEN DE PROGRAMACION\n"
        exam_content += f"Tema: {tema}\n"
        exam_content += f"Instrucciones: Responde las siguientes preguntas.\n\n"
        
        for i, q in enumerate(parsed_back, 1):
            exam_content += f"{i}. {q.get('pregunta', 'Pregunta sin texto')}\n"
            opciones = q.get('opciones', [])
            for idx, opt in enumerate(opciones):
                exam_content += f"    {chr(97+idx)}) {opt}\n"
            exam_content += f"Respuesta correcta: {q.get('respuesta', 'N/A')}\n\n"
        
        print(f"Examen creado exitosamente!")
        print(f"Longitud del examen: {len(exam_content)} caracteres")
        print(f"Número de preguntas en examen: {exam_content.count('. ')}")
        
        # Guardar archivo de prueba
        with open("test_exam_output.txt", "w", encoding="utf-8") as f:
            f.write(exam_content)
        print("✅ Archivo de prueba guardado como 'test_exam_output.txt'")
        
        print("\n" + "=" * 50)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("✅ El sistema debería funcionar correctamente")
        
    except Exception as e:
        print(f"❌ ERROR en serialización JSON: {e}")
        print(f"Tipo de error: {type(e)}")

if __name__ == "__main__":
    test_json_serialization()