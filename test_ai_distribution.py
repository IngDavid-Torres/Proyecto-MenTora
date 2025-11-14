#!/usr/bin/env python3
"""
Script de prueba para verificar la distribución de respuestas correctas
en el generador de IA local
"""

from ai_local import LocalAIExamGenerator

def test_answer_distribution():
    """Prueba la distribución de respuestas correctas"""
    generator = LocalAIExamGenerator()
    
    print("🧪 Probando distribución de respuestas correctas...")
    print("=" * 50)
    
    # Probar diferentes temas
    temas = ['programacion', 'matematicas', 'ciencias', 'historia', 'literatura']
    
    for tema in temas:
        print(f"\n📚 Tema: {tema.upper()}")
        print("-" * 30)
        
        # Generar 10 preguntas para ver la distribución
        questions = generator.generate_offline(tema, 10, 'opciones')
        
        # Contar distribución de respuestas
        distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        
        for i, q in enumerate(questions, 1):
            if isinstance(q, dict) and 'respuesta' in q:
                respuesta = q['respuesta']
                distribution[respuesta] += 1
                print(f"   Pregunta {i}: Respuesta correcta = {respuesta}")
                print(f"   📝 {q['pregunta'][:60]}...")
                print(f"   🅰️ A) {q['opciones'][0][:30]}...")
                print(f"   🅱️ B) {q['opciones'][1][:30]}...")
                print(f"   🅲️ C) {q['opciones'][2][:30]}...")
                print(f"   🅳️ D) {q['opciones'][3][:30]}...")
                print(f"   ✅ Correcta: {respuesta}")
                print()
        
        print(f"📊 Distribución de respuestas para {tema}:")
        total = sum(distribution.values())
        for letra, count in distribution.items():
            porcentaje = (count / total * 100) if total > 0 else 0
            print(f"   {letra}: {count}/10 ({porcentaje:.1f}%)")
        
        print()

def test_specific_subjects():
    """Prueba preguntas específicas por materia"""
    generator = LocalAIExamGenerator()
    
    print("\n🔬 Probando preguntas específicas por materia...")
    print("=" * 50)
    
    # Probar programación específicamente
    print("\n💻 PROGRAMACIÓN:")
    prog_questions = generator.generate_offline('programacion', 3, 'opciones')
    for i, q in enumerate(prog_questions, 1):
        if isinstance(q, dict):
            print(f"Pregunta {i}: {q['pregunta']}")
            for j, opcion in enumerate(q['opciones']):
                letra = chr(65 + j)
                marca = "✅" if letra == q['respuesta'] else "  "
                print(f"  {marca} {letra}) {opcion}")
            print()
    
    # Probar ciencias
    print("\n🔬 CIENCIAS:")
    sci_questions = generator.generate_offline('ciencias', 3, 'opciones')
    for i, q in enumerate(sci_questions, 1):
        if isinstance(q, dict):
            print(f"Pregunta {i}: {q['pregunta']}")
            for j, opcion in enumerate(q['opciones']):
                letra = chr(65 + j)
                marca = "✅" if letra == q['respuesta'] else "  "
                print(f"  {marca} {letra}) {opcion}")
            print()

if __name__ == "__main__":
    try:
        test_answer_distribution()
        test_specific_subjects()
        print("✅ Todas las pruebas completadas exitosamente!")
        print("\n💡 Ahora las respuestas correctas deberían estar distribuidas")
        print("   de manera más equilibrada entre A, B, C y D.")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()