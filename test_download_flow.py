#!/usr/bin/env python3
"""
Script de prueba para verificar el flujo completo de descarga TXT
Simula exactamente lo que hace la aplicación Flask
"""
import sys
import json
from io import BytesIO

# Añadir el directorio actual al path
sys.path.append('.')

def test_complete_flow():
    print("=== TEST COMPLETO DEL FLUJO DE DESCARGA ===\n")
    
    try:
        # Paso 1: Importar módulos necesarios
        from ai_local import generate_local_exam
        from exam_utils import create_text_exam, debug_preguntas_info
        
        # Paso 2: Simular la generación desde teacher_dashboard (POST request)
        print("1. SIMULANDO GENERACION EN TEACHER_DASHBOARD")
        tema = "programación"
        cantidad = 5
        tipo_examen = "opciones"
        ai_method = "offline"
        
        print(f"   Tema: {tema}")
        print(f"   Cantidad: {cantidad}")
        print(f"   Tipo: {tipo_examen}")
        print(f"   Método: {ai_method}")
        
        # Generar preguntas (como en teacher_dashboard)
        ia_questions = generate_local_exam(tema, cantidad, tipo_examen, ai_method)
        
        if not ia_questions:
            print("   ERROR: No se generaron preguntas")
            return False
            
        print(f"   ✓ Generadas {len(ia_questions)} preguntas")
        
        # Mostrar las preguntas generadas
        print("\n   PREGUNTAS GENERADAS:")
        for i, q in enumerate(ia_questions[:3], 1):  # Solo primeras 3
            print(f"   {i}. {q['pregunta']}")
        print(f"   ... y {len(ia_questions)-3} más")
        
        # Paso 3: Simular el template safe_json filter
        print("\n2. SIMULANDO TEMPLATE SAFE_JSON FILTER")
        
        # Aplicar el filtro safe_json exactamente como en la aplicación
        json_str = json.dumps(ia_questions, ensure_ascii=True, separators=(',', ':'))
        print(f"   ✓ JSON serializado: {len(json_str)} caracteres")
        print(f"   Preview: {json_str[:100]}...")
        
        # Paso 4: Simular el formulario HTML
        print("\n3. SIMULANDO ENVIO DEL FORMULARIO HTML")
        
        # Estos serían los datos del formulario POST a download_exam_simple
        form_data = {
            'tema': tema,
            'area': 'Tecnología',  # Como estaría en el formulario
            'tipo_examen': tipo_examen,
            'preguntas': json_str  # Este es el campo hidden con ia_questions|safe_json
        }
        
        print(f"   Tema form: {form_data['tema']}")
        print(f"   Area form: {form_data['area']}")
        print(f"   Tipo form: {form_data['tipo_examen']}")
        print(f"   Preguntas form length: {len(form_data['preguntas'])}")
        
        # Paso 5: Simular download_exam_simple
        print("\n4. SIMULANDO DOWNLOAD_EXAM_SIMPLE")
        
        # Extraer datos del formulario (como en la función real)
        tema_form = form_data.get('tema', 'Examen')
        area_form = form_data.get('area', 'General') 
        tipo_examen_form = form_data.get('tipo_examen', 'simple')
        preguntas_raw = form_data.get('preguntas', '')
        
        print(f"   Datos extraídos del form:")
        print(f"     Tema: {tema_form}")
        print(f"     Area: {area_form}")
        print(f"     Tipo: {tipo_examen_form}")
        print(f"     Preguntas raw: {len(preguntas_raw)} chars")
        
        # Debug como en la función real
        debug_info = debug_preguntas_info(preguntas_raw)
        print(f"   Debug info: {debug_info}")
        
        # Intentar parsear JSON
        try:
            if not preguntas_raw or preguntas_raw.strip() == '':
                raise ValueError("Preguntas raw está vacío")
            
            preguntas_parsed = json.loads(preguntas_raw)
            print(f"   ✓ JSON parseado exitosamente: {len(preguntas_parsed)} preguntas")
            
            if isinstance(preguntas_parsed, list) and len(preguntas_parsed) > 0:
                primera = preguntas_parsed[0]
                print(f"   Primera pregunta: {primera['pregunta'][:50]}...")
                
                # Verificar que es de programación
                if isinstance(primera, dict) and 'pregunta' in primera:
                    pregunta_texto = primera['pregunta'].lower()
                    es_programacion = any(palabra in pregunta_texto for palabra in 
                                        ['función', 'variable', 'código', 'programa', 'algoritmo', 
                                         'python', 'javascript', 'java', 'php', 'c++', 'c#', 
                                         'operador', 'sintaxis', 'tipo de dato', 'ventajas'])
                    print(f"   ✓ Es pregunta de programación: {es_programacion}")
                    
                    if es_programacion:
                        preguntas_finales = preguntas_parsed
                        origen = "JSON original"
                    else:
                        print("   WARN: No detectada como programación, usando fallback")
                        preguntas_finales = generate_local_exam("programacion", 5, tipo_examen_form, "offline")
                        origen = "Fallback IA"
                else:
                    print("   ERROR: Formato de pregunta inválido")
                    preguntas_finales = generate_local_exam("programacion", 5, tipo_examen_form, "offline")
                    origen = "Fallback por formato inválido"
            else:
                print("   ERROR: Lista vacía o formato inválido")
                preguntas_finales = generate_local_exam("programacion", 5, tipo_examen_form, "offline")
                origen = "Fallback por lista vacía"
                
        except Exception as e:
            print(f"   ERROR parseando JSON: {e}")
            preguntas_finales = generate_local_exam("programacion", 5, tipo_examen_form, "offline")
            origen = "Fallback por error de parsing"
        
        print(f"   ✓ Preguntas finales ({origen}): {len(preguntas_finales)} preguntas")
        
        # Paso 6: Crear contenido TXT
        print("\n5. CREANDO CONTENIDO TXT FINAL")
        
        content = create_text_exam(tema_form, area_form, tipo_examen_form, preguntas_finales)
        
        # Crear archivo en memoria
        archivo_bytes = content.encode('utf-8')
        filename = f"Examen_{area_form}_{tema_form}_simple.txt".replace(' ', '_').replace('/', '_')
        
        print(f"   ✓ Contenido creado: {len(content)} caracteres")
        print(f"   ✓ Archivo: {filename} ({len(archivo_bytes)} bytes)")
        
        # Mostrar preview del contenido
        print(f"\n6. PREVIEW DEL ARCHIVO TXT:")
        print("-" * 50)
        lineas = content.split('\n')
        for i, linea in enumerate(lineas[:25]):  # Primeras 25 líneas
            print(linea)
        
        if len(lineas) > 25:
            print(f"... y {len(lineas)-25} líneas más")
        
        print("-" * 50)
        
        # Verificar si el contenido es correcto
        es_correcto = False
        if "EXAMEN DE TECNOLOGIA" in content and "programacion" in content.lower():
            # Buscar preguntas específicas de programación
            contenido_lower = content.lower()
            palabras_programacion = ['función', 'variable', 'python', 'javascript', 'java', 
                                   'operador', 'sintaxis', 'algoritmo', 'ventajas']
            
            encontradas = sum(1 for palabra in palabras_programacion if palabra in contenido_lower)
            if encontradas >= 2:  # Al menos 2 palabras de programación
                es_correcto = True
                print(f"\n✓ EXITO: El archivo contiene preguntas reales de programación")
                print(f"  Palabras técnicas encontradas: {encontradas}")
            else:
                print(f"\n✗ FALLO: El archivo no contiene suficientes términos de programación")
                print(f"  Solo {encontradas} palabras técnicas encontradas")
        else:
            print(f"\n✗ FALLO: El archivo no tiene el formato esperado")
        
        # Opcionalmente guardar archivo para inspección
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n📁 Archivo guardado para inspección: {filename}")
        except Exception as e:
            print(f"\n⚠️  No se pudo guardar archivo: {e}")
        
        return es_correcto
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    print(f"\n{'='*60}")
    if success:
        print("🎉 TEST EXITOSO: La descarga TXT debería funcionar correctamente")
    else:
        print("❌ TEST FALLIDO: Hay problemas en el flujo de descarga")
    print(f"{'='*60}")