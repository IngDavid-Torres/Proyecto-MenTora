# Script de prueba para verificar el funcionamiento completo
import sys
import os
sys.path.append(r'c:\Users\doser\OneDrive\Escritorio\MenTora')

from ai_local import generate_local_exam
from exam_utils import create_text_exam, debug_preguntas_info
import json

def test_exam_generation():
    print("=" * 60)
    print("PRUEBA COMPLETA DEL SISTEMA DE EXAMENES")
    print("=" * 60)
    
    # Probar generación de exámenes de programación
    print("\n1. GENERANDO EXAMENES DE PROGRAMACION...")
    
    # Prueba con opciones múltiples
    print("\n   📋 Examen con opciones múltiples:")
    questions_opciones = generate_local_exam("programación", 5, "opciones", "offline")
    print(f"   ✅ Generadas: {len(questions_opciones)} preguntas")
    
    # Prueba serialización JSON
    json_str = json.dumps(questions_opciones, ensure_ascii=False)
    print(f"   ✅ JSON serialization: {len(json_str)} caracteres")
    
    # Prueba deserialización
    parsed = json.loads(json_str)
    print(f"   ✅ JSON deserialization: {len(parsed)} preguntas")
    
    # Crear examen de texto
    content = create_text_exam("programación", "Informática", "opciones", questions_opciones)
    print(f"   ✅ Examen de texto creado: {len(content)} caracteres")
    
    print("\n   📋 Examen simple:")
    questions_simple = generate_local_exam("programación", 3, "simple", "offline")
    print(f"   ✅ Generadas: {len(questions_simple)} preguntas simples")
    
    print("\n2. MOSTRANDO EJEMPLOS...")
    print("\n   📝 PRIMERA PREGUNTA CON OPCIONES:")
    if questions_opciones:
        q = questions_opciones[0]
        print(f"   Pregunta: {q['pregunta']}")
        for i, opt in enumerate(q['opciones']):
            print(f"   {chr(65+i)}) {opt}")
        print(f"   Respuesta: {q['respuesta']}")
    
    print("\n   📝 PRIMERA PREGUNTA SIMPLE:")
    if questions_simple:
        print(f"   {questions_simple[0]}")
    
    print("\n3. SIMULANDO DESCARGA...")
    
    # Simular el proceso completo como en la app
    tema = "programación"
    area = "Informática"
    tipo_examen = "opciones"
    
    # Simular serialización como en el template
    preguntas_raw = json.dumps(questions_opciones, ensure_ascii=False)
    
    # Simular debug info
    debug_info = debug_preguntas_info(preguntas_raw)
    print(f"   📊 Debug info: {debug_info}")
    
    # Simular creación de archivo
    final_content = create_text_exam(tema, area, tipo_examen, questions_opciones)
    filename = f"Examen_{area}_{tema}_test.txt"
    
    # Escribir archivo de prueba
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"   ✅ Archivo de prueba creado: {filename}")
    print(f"   📏 Tamaño: {len(final_content)} caracteres")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("✅ El sistema puede generar y descargar exámenes completos")
    print("=" * 60)

if __name__ == "__main__":
    test_exam_generation()