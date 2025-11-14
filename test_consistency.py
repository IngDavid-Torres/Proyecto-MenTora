#!/usr/bin/env python3
"""
Script de prueba para verificar la consistencia de preguntas entre generación y descarga.
Este script simula el flujo completo de la aplicación web.
"""

import json
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simulate_web_flow():
    """Simula el flujo completo de generación y descarga de exámenes"""
    print("=== SIMULACIÓN DEL FLUJO WEB COMPLETO ===")
    
    # Paso 1: Generar preguntas (como en teacher_dashboard)
    print("\n1. GENERANDO PREGUNTAS EN EL DASHBOARD...")
    try:
        from ai_local import generate_local_exam
        
        tema = "programacion"
        cantidad = 5
        tipo_examen = "opciones"
        ai_method = "offline"
        
        print(f"Parámetros: tema={tema}, cantidad={cantidad}, tipo={tipo_examen}, método={ai_method}")
        
        # Generar preguntas
        ia_questions = generate_local_exam(tema, cantidad, tipo_examen, ai_method)
        
        if ia_questions:
            print(f"✅ Preguntas generadas exitosamente: {len(ia_questions)}")
            
            # Mostrar las preguntas generadas
            for i, q in enumerate(ia_questions):
                print(f"  Pregunta {i+1}: {q.get('pregunta', 'Sin pregunta')[:50]}...")
                
        else:
            print("❌ No se generaron preguntas")
            return False
            
    except Exception as e:
        print(f"❌ Error generando preguntas: {e}")
        return False
    
    # Paso 2: Serializar para el formulario (como en la plantilla)
    print("\n2. SERIALIZANDO PARA EL FORMULARIO...")
    try:
        # Usar la misma función que la plantilla
        serialized_questions = json.dumps(ia_questions, ensure_ascii=True, separators=(',', ':'))
        print(f"✅ Preguntas serializadas: {len(serialized_questions)} caracteres")
        print(f"Inicio del JSON: {serialized_questions[:100]}...")
        
    except Exception as e:
        print(f"❌ Error serializando: {e}")
        return False
    
    # Paso 3: Simular envío del formulario y parseo (como en download functions)
    print("\n3. SIMULANDO RECEPCIÓN EN DESCARGA...")
    try:
        # Simular request.form.get('preguntas', '')
        preguntas_raw = serialized_questions
        
        print(f"Datos recibidos: {len(preguntas_raw)} caracteres")
        
        # Parsear usando la misma lógica que las funciones de descarga
        preguntas_clean = preguntas_raw.strip()
        
        if preguntas_clean.startswith('[') and preguntas_clean.endswith(']'):
            preguntas_parsed = json.loads(preguntas_clean)
        else:
            print("❌ Formato JSON no reconocido")
            return False
            
        print(f"✅ Preguntas parseadas: {len(preguntas_parsed)}")
        
        # Verificar que son las mismas preguntas
        for i, (original, parsed) in enumerate(zip(ia_questions, preguntas_parsed)):
            original_pregunta = original.get('pregunta', '')
            parsed_pregunta = parsed.get('pregunta', '')
            
            if original_pregunta == parsed_pregunta:
                print(f"  ✅ Pregunta {i+1}: COINCIDE")
            else:
                print(f"  ❌ Pregunta {i+1}: NO COINCIDE")
                print(f"    Original: {original_pregunta[:50]}...")
                print(f"    Parseada: {parsed_pregunta[:50]}...")
                return False
                
    except Exception as e:
        print(f"❌ Error en parseo: {e}")
        return False
    
    # Paso 4: Generar contenido de descarga
    print("\n4. GENERANDO CONTENIDO DE DESCARGA...")
    try:
        from exam_utils import create_text_exam
        
        content = create_text_exam(tema, "Programación", tipo_examen, preguntas_parsed)
        
        print(f"✅ Contenido generado: {len(content)} caracteres")
        print("Primeras líneas del examen:")
        for line in content.split('\n')[:10]:
            if line.strip():
                print(f"  {line}")
                
    except Exception as e:
        print(f"❌ Error generando contenido: {e}")
        return False
    
    return True

def test_json_consistency():
    """Prueba específica de consistencia JSON"""
    print("\n=== PRUEBA DE CONSISTENCIA JSON ===")
    
    # Crear preguntas de prueba
    test_questions = [
        {
            'pregunta': '¿Qué es una variable en programación?',
            'opciones': [
                'Un contenedor de datos',
                'Una función matemática', 
                'Un tipo de bucle',
                'Una condición lógica'
            ],
            'respuesta': 'A'
        },
        {
            'pregunta': '¿Cuál es la diferencia entre "==" y "==="?',
            'opciones': [
                'No hay diferencia',
                '== compara valor, === compara valor y tipo',
                '=== es para números solamente',
                '== es más rápido que ==='
            ],
            'respuesta': 'B'
        }
    ]
    
    print(f"Preguntas originales: {len(test_questions)}")
    
    # Ciclo completo de serialización/deserialización
    try:
        # 1. Serializar (frontend)
        serialized = json.dumps(test_questions, ensure_ascii=True, separators=(',', ':'))
        print(f"✅ Serializado: {len(serialized)} caracteres")
        
        # 2. Deserializar (backend)
        deserialized = json.loads(serialized)
        print(f"✅ Deserializado: {len(deserialized)} preguntas")
        
        # 3. Verificar integridad
        if len(test_questions) == len(deserialized):
            print("✅ Cantidad de preguntas: CORRECTA")
        else:
            print("❌ Cantidad de preguntas: INCORRECTA")
            return False
            
        for i, (orig, deser) in enumerate(zip(test_questions, deserialized)):
            if orig['pregunta'] == deser['pregunta']:
                print(f"✅ Pregunta {i+1}: TEXTO CORRECTO")
            else:
                print(f"❌ Pregunta {i+1}: TEXTO INCORRECTO")
                return False
                
            if orig['respuesta'] == deser['respuesta']:
                print(f"✅ Pregunta {i+1}: RESPUESTA CORRECTA")
            else:
                print(f"❌ Pregunta {i+1}: RESPUESTA INCORRECTA")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Error en consistencia JSON: {e}")
        return False

def main():
    """Ejecuta todas las pruebas de consistencia"""
    print("PRUEBAS DE CONSISTENCIA DE PREGUNTAS")
    print("=" * 50)
    
    # Prueba 1: Consistencia JSON
    json_ok = test_json_consistency()
    
    # Prueba 2: Flujo web completo
    flow_ok = simulate_web_flow()
    
    # Resultados
    print("\n" + "=" * 50)
    print("RESULTADOS FINALES:")
    print(f"✅ Consistencia JSON: {'EXITOSA' if json_ok else 'FALLIDA'}")
    print(f"✅ Flujo Web Completo: {'EXITOSO' if flow_ok else 'FALLIDO'}")
    
    if json_ok and flow_ok:
        print("\n🎉 TODAS LAS PRUEBAS DE CONSISTENCIA PASARON")
        print("Las preguntas se mantienen íntegras desde la generación hasta la descarga.")
    else:
        print("\n⚠️  PROBLEMA DE CONSISTENCIA DETECTADO")
        print("Las preguntas no se mantienen consistentes en el flujo completo.")
        
    return json_ok and flow_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)