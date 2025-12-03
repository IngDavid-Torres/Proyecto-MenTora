#!/usr/bin/env python3
"""
Test script para verificar la generación de exámenes con IA local.
Este script prueba la funcionalidad completa sin necesidad del servidor web.
"""

import json
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_json_serialization():
    """Prueba la serialización JSON usando el mismo método que la plantilla."""
    print("=== PRUEBA DE SERIALIZACIÓN JSON ===")
    
    # Simular datos de preguntas como los genera la IA
    preguntas_test = [
        {
            'pregunta': '¿Cuál es la principal diferencia entre una variable y una constante en programación?',
            'opciones': [
                'Las variables pueden cambiar su valor, las constantes no',
                'Las constantes son más rápidas que las variables',
                'No hay diferencia entre ellas',
                'Las variables solo almacenan números'
            ],
            'respuesta': 'A'
        },
        {
            'pregunta': '¿Qué significa "debugging" en programación?',
            'opciones': [
                'Crear nuevos programas',
                'Encontrar y corregir errores en el código',
                'Compilar el programa',
                'Documentar el código'
            ],
            'respuesta': 'B'
        }
    ]
    
    print(f"Preguntas originales: {len(preguntas_test)}")
    
    # Probar serialización con json.dumps (método safe_json)
    try:
        json_string = json.dumps(preguntas_test, ensure_ascii=True, separators=(',', ':'))
        print(f"✅ Serialización con json.dumps: EXITOSA")
        print(f"Longitud del JSON: {len(json_string)}")
        print(f"Primeros 100 caracteres: {json_string[:100]}...")
        
        # Probar deserialización
        preguntas_recuperadas = json.loads(json_string)
        print(f"✅ Deserialización: EXITOSA - {len(preguntas_recuperadas)} preguntas recuperadas")
        
        return json_string
        
    except Exception as e:
        print(f"❌ Error en serialización JSON: {e}")
        return None

def test_local_ai_generation():
    """Prueba la generación de exámenes con IA local."""
    print("\n=== PRUEBA DE GENERACIÓN IA LOCAL ===")
    
    try:
        from ai_local import LocalAIExamGenerator
        print("✅ Módulo ai_local importado correctamente")
        
        # Crear instancia del generador
        generator = LocalAIExamGenerator()
        print("✅ Generador IA Local inicializado")
        
        # Probar generación con templates (método más confiable)
        tema = "programacion"
        num_preguntas = 3
        tipo_examen = "opciones"
        metodo = "offline"
        
        print(f"Generando examen: tema={tema}, preguntas={num_preguntas}, tipo={tipo_examen}, método={metodo}")
        
        preguntas = generator.generate_exam(tema, num_preguntas, tipo_examen, metodo)
        
        if preguntas and len(preguntas) > 0:
            print(f"✅ Generación exitosa: {len(preguntas)} preguntas generadas")
            
            # Verificar estructura
            for i, pregunta in enumerate(preguntas):
                if isinstance(pregunta, dict):
                    keys = list(pregunta.keys())
                    print(f"  Pregunta {i+1}: keys={keys}")
                    if 'pregunta' in pregunta:
                        print(f"    Texto: {pregunta['pregunta'][:60]}...")
                else:
                    print(f"  ❌ Pregunta {i+1}: formato incorrecto - {type(pregunta)}")
            
            return preguntas
        else:
            print(f"❌ No se generaron preguntas: {preguntas}")
            return None
            
    except ImportError as e:
        print(f"❌ Error importando ai_local: {e}")
        return None
    except Exception as e:
        print(f"❌ Error en generación IA: {e}")
        return None

def test_json_parsing_robustness():
    """Prueba diferentes formatos de JSON que pueden causar problemas."""
    print("\n=== PRUEBA DE ROBUSTEZ JSON ===")
    
    # Casos de prueba problemáticos
    test_cases = [
        # JSON válido
        '[{"pregunta": "Test", "opciones": ["A", "B"], "respuesta": "A"}]',
        
        # JSON con comillas simples (problemático)
        "[{'pregunta': 'Test', 'opciones': ['A', 'B'], 'respuesta': 'A'}]",
        
        # JSON con espacios extra
        '[ { "pregunta" : "Test" , "opciones" : [ "A" , "B" ] , "respuesta" : "A" } ]',
        
        # JSON con caracteres especiales
        '[{"pregunta": "¿Qué es programación?", "opciones": ["A", "B"], "respuesta": "A"}]',
    ]
    
    for i, test_json in enumerate(test_cases):
        print(f"\nCaso {i+1}: {test_json[:50]}...")
        
        try:
            # Método 1: json.loads directo
            preguntas = json.loads(test_json)
            print(f"  ✅ json.loads: {len(preguntas)} preguntas")
        except json.JSONDecodeError as e:
            print(f"  ❌ json.loads falló: {e}")
            
            try:
                # Método 2: reparar y reintentar
                repaired = test_json.replace("'", '"')
                preguntas = json.loads(repaired)
                print(f"  ✅ JSON reparado: {len(preguntas)} preguntas")
            except json.JSONDecodeError as e2:
                print(f"  ❌ Reparación falló: {e2}")
                
                try:
                    # Método 3: ast.literal_eval
                    import ast
                    preguntas = ast.literal_eval(test_json)
                    print(f"  ✅ ast.literal_eval: {len(preguntas)} preguntas")
                except (ValueError, SyntaxError) as e3:
                    print(f"  ❌ ast también falló: {e3}")

def main():
    """Ejecuta todas las pruebas."""
    print("INICIANDO PRUEBAS DE GENERACIÓN DE EXÁMENES")
    print("=" * 50)
    
    # Prueba 1: Serialización JSON
    json_result = test_json_serialization()
    
    # Prueba 2: Generación IA Local
    ai_result = test_local_ai_generation()
    
    # Prueba 3: Robustez JSON
    test_json_parsing_robustness()
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE PRUEBAS:")
    print(f"✅ Serialización JSON: {'EXITOSA' if json_result else 'FALLIDA'}")
    print(f"✅ Generación IA Local: {'EXITOSA' if ai_result else 'FALLIDA'}")
    
    if json_result and ai_result:
        print("\n🎉 TODAS LAS PRUEBAS BÁSICAS PASARON")
        print("El sistema debería funcionar correctamente para generar y descargar exámenes.")
        
        # Prueba integrada: serializar preguntas generadas
        print("\n=== PRUEBA INTEGRADA ===")
        try:
            json_integrado = json.dumps(ai_result, ensure_ascii=True, separators=(',', ':'))
            preguntas_final = json.loads(json_integrado)
            print(f"✅ Integración completa: {len(preguntas_final)} preguntas procesadas correctamente")
        except Exception as e:
            print(f"❌ Error en integración: {e}")
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
        print("Revisa los errores anteriores para resolver problemas.")

if __name__ == "__main__":
    main()