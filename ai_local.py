"""
Generador de exámenes con IA local para MenTora
Soporta múltiples métodos: Ollama, Hugging Face y plantillas
"""
import json
import random
import requests
from typing import List, Dict, Optional

class LocalAIExamGenerator:
    def __init__(self):
        self.question_templates = {
            'matematicas': [
                "¿Cuál es el resultado de {num1} + {num2}?",
                "Si tengo {num1} manzanas y compro {num2} más, ¿cuántas tengo en total?",
                "¿Cuánto es {num1} × {num2}?",
                "Resuelve: {num1} - {num2} = ?",
                "¿Cuál es el {percent}% de {num1}?",
            ],
            'programacion': [
                "¿Qué hace la función {function} en {language}?",
                "¿Cuál es la diferencia entre {concept1} y {concept2} en programación?",
                "¿Qué tipo de dato devuelve {method} en {language}?",
                "¿Para qué se utiliza {structure} en programación?",
                "¿Cuál es la sintaxis correcta para {operation} en {language}?",
                "¿Qué significa {term} en el contexto de {paradigm}?",
                "¿Cuál es la complejidad temporal de {algorithm}?",
                "¿Qué patrón de diseño resuelve el problema de {problem}?",
                "¿En qué se diferencia {language1} de {language2}?",
                "¿Qué es {concept} y cuándo se utiliza?",
                "¿Cómo se implementa {feature} en {language}?",
                "¿Qué ventajas tiene {technology} sobre {alternative}?",
                "¿Cuál es el propósito de {keyword} en {language}?",
                "¿Qué hace el operador {operator} en {language}?",
                "¿Cómo se maneja {error_type} en programación?"
            ],
            'ciencias': [
                "¿Cuál es la fórmula química del {compound}?",
                "¿En qué año se descubrió {discovery}?",
                "¿Cuál es la función principal del {organ} en el cuerpo humano?",
                "¿Qué gas representa el {percent}% de la atmósfera?",
                "¿Cuál es la velocidad de la luz en el vacío?",
            ],
            'historia': [
                "¿En qué año ocurrió {event}?",
                "¿Quién fue {historical_figure} y por qué es importante?",
                "¿Cuáles fueron las causas principales de {war}?",
                "¿En qué siglo se desarrolló {period}?",
                "¿Qué país colonizó {territory}?",
            ],
            'literatura': [
                "¿Quién escribió '{book}'?",
                "¿Cuál es el tema principal de '{book}'?",
                "¿En qué siglo vivió {author}?",
                "¿Qué movimiento literario representa {author}?",
                "¿Cuál es la moraleja de '{story}'?",
            ],
            'geografia': [
                "¿Cuál es la capital de {country}?",
                "¿En qué continente se encuentra {country}?",
                "¿Cuál es el río más largo de {continent}?",
                "¿Qué océano baña las costas de {country}?",
                "¿Cuál es la montaña más alta de {continent}?",
            ]
        }
        
        self.knowledge_base = {
            'matematicas': {
                'num1': list(range(1, 100)),
                'num2': list(range(1, 50)),
                'percent': [10, 20, 25, 30, 40, 50, 75, 80, 90]
            },
            'programacion': {
                'function': ['print()', 'len()', 'input()', 'range()', 'append()', 'split()', 'join()', 'sort()'],
                'language': ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby'],
                'concept1': ['variable', 'función', 'clase', 'objeto', 'array', 'lista'],
                'concept2': ['constante', 'método', 'instancia', 'atributo', 'tupla', 'diccionario'],
                'method': ['substring()', 'charAt()', 'indexOf()', 'replace()', 'toLowerCase()', 'toUpperCase()'],
                'structure': ['arrays', 'listas enlazadas', 'pilas', 'colas', 'árboles', 'grafos', 'hash tables'],
                'operation': ['declarar una variable', 'crear un bucle for', 'definir una función', 'crear una clase'],
                'term': ['polimorfismo', 'herencia', 'encapsulación', 'abstracción', 'recursión', 'iteración'],
                'paradigm': ['programación orientada a objetos', 'programación funcional', 'programación estructurada'],
                'algorithm': ['búsqueda binaria', 'ordenamiento burbuja', 'quicksort', 'mergesort', 'búsqueda lineal'],
                'problem': ['creación de objetos', 'notificación de cambios', 'acceso a datos', 'estado de objeto'],
                'language1': ['Python', 'JavaScript', 'Java', 'C++'],
                'language2': ['R', 'PHP', 'C#', 'Ruby'],
                'concept': ['API REST', 'base de datos', 'framework', 'biblioteca', 'git', 'debugging'],
                'feature': ['herencia múltiple', 'decoradores', 'lambdas', 'generators', 'async/await'],
                'technology': ['React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring'],
                'alternative': ['jQuery', 'Vanilla JS', 'Ruby on Rails', 'Laravel', 'Express.js'],
                'keyword': ['this', 'super', 'static', 'final', 'abstract', 'interface', 'extends'],
                'operator': ['++', '--', '==', '===', '&&', '||', '?:', '>>'],
                'error_type': ['excepciones', 'errores de sintaxis', 'errores de lógica', 'memory leaks']
            },
            'ciencias': {
                'compound': ['agua', 'dióxido de carbono', 'sal', 'oxígeno', 'metano'],
                'discovery': ['la penicilina', 'la electricidad', 'el ADN', 'la radioactividad'],
                'organ': ['corazón', 'cerebro', 'hígado', 'riñones', 'pulmones'],
                'percent': [21, 78, 1]
            },
            'historia': {
                'event': ['la Independencia de México', 'la Revolución Francesa', 'la Segunda Guerra Mundial'],
                'historical_figure': ['Benito Juárez', 'Miguel Hidalgo', 'Napoleón Bonaparte'],
                'war': ['la Primera Guerra Mundial', 'la Guerra de Independencia'],
                'period': ['el Renacimiento', 'la Edad Media', 'la Ilustración'],
                'territory': ['México', 'Brasil', 'India', 'Australia']
            },
            'literatura': {
                'book': ['Don Quijote', 'Cien años de soledad', 'La Divina Comedia'],
                'author': ['Cervantes', 'García Márquez', 'Shakespeare', 'Sor Juana'],
                'story': ['La Cenicienta', 'Los Tres Cerditos', 'Caperucita Roja']
            },
            'geografia': {
                'country': ['México', 'Brasil', 'España', 'Francia', 'Italia', 'Alemania'],
                'continent': ['América', 'Europa', 'Asia', 'África', 'Oceanía'],
            }
        }

    def generate_with_ollama(self, tema: str, cantidad: int, tipo_examen: str = 'simple') -> List[Dict]:
        """Genera exámenes usando Ollama (requiere Ollama instalado)"""
        try:
            if tipo_examen == 'opciones':
                prompt = f"""Genera {cantidad} preguntas de opción múltiple sobre {tema} para estudiantes de nivel medio.
Cada pregunta debe tener:
- Una pregunta clara
- 4 opciones (A, B, C, D)
- La respuesta correcta
Formato: pregunta|opcionA|opcionB|opcionC|opcionD|respuesta_correcta"""
            else:
                prompt = f"Genera {cantidad} preguntas abiertas sobre {tema} para estudiantes de nivel medio. Una pregunta por línea."

            response = requests.post('http://localhost:11434/api/generate', 
                json={
                    'model': 'llama3.2',  # o 'mistral', 'gemma'
                    'prompt': prompt,
                    'stream': False
                })
            
            if response.status_code == 200:
                text = response.json()['response']
                return self._parse_ollama_response(text, tipo_examen)
            else:
                print("Ollama no disponible, usando generador offline...")
                return self.generate_offline(tema, cantidad, tipo_examen)
                
        except Exception as e:
            print(f"Error con Ollama: {e}, usando generador offline...")
            return self.generate_offline(tema, cantidad, tipo_examen)

    def generate_with_huggingface(self, tema: str, cantidad: int, tipo_examen: str = 'simple') -> List[Dict]:
        """Genera exámenes usando modelos de Hugging Face locales"""
        try:
            from transformers import pipeline, set_seed
            
            # Usar un modelo de generación de texto liviano
            generator = pipeline('text-generation', 
                               model='microsoft/DialoGPT-medium',
                               tokenizer='microsoft/DialoGPT-medium')
            
            questions = []
            set_seed(42)
            # Limitar cantidad a rango seguro
            safe_cantidad = min(max(int(cantidad), 1), 20) if str(cantidad).isdigit() else 5
            for i in range(safe_cantidad):
                if tipo_examen == 'opciones':
                    prompt = f"Pregunta de opción múltiple sobre {tema}:"
                else:
                    prompt = f"Pregunta sobre {tema}:"
                result = generator(prompt, max_length=100, num_return_sequences=1)
                question_text = result[0]['generated_text'].replace(prompt, '').strip()
                
                if tipo_examen == 'opciones':
                    questions.append({
                        'pregunta': question_text,
                        'opciones': [
                            f"Opción A para {tema}",
                            f"Opción B para {tema}", 
                            f"Opción C para {tema}",
                            f"Opción D para {tema}"
                        ],
                        'respuesta': 'A'
                    })
                else:
                    questions.append(question_text)
            
            return questions
            
        except Exception as e:
            print(f"Error con Hugging Face: {e}, usando generador offline...")
            return self.generate_offline(tema, cantidad, tipo_examen)

    def generate_offline(self, tema: str, cantidad: int, tipo_examen: str = 'simple') -> List[Dict]:
        """Generador offline usando plantillas y base de conocimiento"""
        tema_lower = tema.lower()
        
        # Normalizar el tema eliminando acentos y caracteres especiales
        import unicodedata
        tema_normalized = unicodedata.normalize('NFD', tema_lower)
        tema_normalized = ''.join(char for char in tema_normalized if unicodedata.category(char) != 'Mn')
        
        # Buscar el tema más cercano con múltiples criterios
        tema_key = None
        
        # Mapeo de sinónimos para mejorar la detección
        tema_synonyms = {
            'programacion': ['programacion', 'programación', 'programming', 'codigo', 'código', 'software', 'desarrollo'],
            'matematicas': ['matematicas', 'matemáticas', 'math', 'aritmetica', 'aritmética', 'algebra', 'álgebra'],
            'ciencias': ['ciencias', 'ciencia', 'science', 'biologia', 'biología', 'fisica', 'física', 'quimica', 'química'],
            'historia': ['historia', 'history', 'historico', 'histórico'],
            'literatura': ['literatura', 'literature', 'letras', 'escritura'],
            'geografia': ['geografia', 'geografía', 'geography', 'paises', 'países']
        }
        
        # Buscar por sinónimos
        for key, synonyms in tema_synonyms.items():
            if any(syn in tema_normalized for syn in synonyms) or any(tema_normalized in syn for syn in synonyms):
                tema_key = key
                break
        
        # Si no se encuentra, buscar en las llaves originales
        if not tema_key:
            for key in self.question_templates.keys():
                if key in tema_normalized or tema_normalized in key:
                    tema_key = key
                    break
        
        # Por defecto usar programación si no se encuentra nada
        if not tema_key:
            tema_key = 'programacion'
        
        templates = self.question_templates[tema_key]
        knowledge = self.knowledge_base[tema_key]
        questions = []
        
        # Limitar cantidad a rango seguro
        safe_cantidad = min(max(int(cantidad), 1), 20) if str(cantidad).isdigit() else 5
        for i in range(safe_cantidad):
            template = random.choice(templates)
            # Rellenar plantilla con datos aleatorios
            filled_question = template
            for placeholder, values in knowledge.items():
                if f'{{{placeholder}}}' in template:
                    filled_question = filled_question.replace(
                        f'{{{placeholder}}}', str(random.choice(values))
                    )
            if tipo_examen == 'opciones':
                # Generar opciones múltiples
                if tema_key == 'matematicas' and any(op in filled_question for op in ['+', '-', '×', '%']):
                    # Para matemáticas, calcular respuesta correcta
                    correct_answer = self._calculate_math_answer(filled_question)
                    wrong_answers = self._generate_wrong_math_answers(correct_answer)
                    
                    opciones = [correct_answer] + wrong_answers
                    random.shuffle(opciones)
                    correct_letter = chr(65 + opciones.index(correct_answer))  # A, B, C, D
                    
                    questions.append({
                        'pregunta': filled_question,
                        'opciones': opciones,
                        'respuesta': correct_letter
                    })
                else:
                    # Para otras materias, opciones genéricas
                    opciones, respuesta_correcta = self._generate_smart_options(tema_key, filled_question, i)
                    questions.append({
                        'pregunta': filled_question,
                        'opciones': opciones,
                        'respuesta': respuesta_correcta
                    })
            else:
                questions.append(filled_question)
        
        return questions

    def _calculate_math_answer(self, question: str) -> str:
        """Calcula la respuesta correcta para preguntas de matemáticas"""
        try:
            # Extraer operación matemática
            if '+' in question:
                nums = [int(x) for x in question.split() if x.isdigit()]
                if len(nums) >= 2:
                    return str(nums[0] + nums[1])
            elif '×' in question or '*' in question:
                nums = [int(x) for x in question.split() if x.isdigit()]
                if len(nums) >= 2:
                    return str(nums[0] * nums[1])
            elif '-' in question:
                nums = [int(x) for x in question.split() if x.isdigit()]
                if len(nums) >= 2:
                    return str(nums[0] - nums[1])
            elif '%' in question:
                nums = [int(x) for x in question.replace('%', ' ').split() if x.isdigit()]
                if len(nums) >= 2:
                    return str(int(nums[0] * nums[1] / 100))
        except:
            pass
        return "42"  # Respuesta por defecto

    def _generate_wrong_math_answers(self, correct: str) -> List[str]:
        """Genera respuestas incorrectas para matemáticas"""
        try:
            num = int(correct)
            wrong = [
                str(num + random.randint(1, 10)),
                str(num - random.randint(1, 10)),
                str(num + random.randint(11, 20))
            ]
            return wrong
        except:
            return ["10", "20", "30"]

    def _generate_generic_options(self, tema: str, question: str) -> List[str]:
        """Genera opciones genéricas basadas en el tema"""
        if tema == 'programacion':
            return self._generate_programming_options(question)
        
        # Opciones más específicas y realistas por tema
        if tema == 'ciencias':
            question_lower = question.lower()
            if 'fórmula' in question_lower or 'formula' in question_lower:
                if 'agua' in question_lower:
                    return ["H2O", "H2SO4", "CO2", "NaCl"]
                elif 'dióxido de carbono' in question_lower or 'dioxido de carbono' in question_lower:
                    return ["CO2", "H2O", "O2", "N2"]
                elif 'sal' in question_lower:
                    return ["NaCl", "H2O", "CO2", "O2"]
                else:
                    return ["H2O", "CO2", "O2", "NaCl"]
            elif 'función' in question_lower or 'funcion' in question_lower:
                if 'corazón' in question_lower or 'corazon' in question_lower:
                    return ["Bombear sangre", "Procesar alimentos", "Filtrar toxinas", "Controlar movimientos"]
                elif 'cerebro' in question_lower:
                    return ["Controlar funciones nerviosas", "Bombear sangre", "Procesar alimentos", "Producir hormonas"]
                elif 'hígado' in question_lower or 'higado' in question_lower:
                    return ["Procesar toxinas", "Bombear sangre", "Controlar respiración", "Producir insulina"]
                else:
                    return ["Función vital específica", "Apoyo estructural", "Almacén de grasa", "Sin función conocida"]
            elif 'velocidad de la luz' in question_lower:
                return ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"]
            elif 'atmósfera' in question_lower or 'atmosfera' in question_lower:
                return ["Nitrógeno (78%)", "Oxígeno (78%)", "CO2 (78%)", "Argón (78%)"]
            else:
                return ["Opción científicamente correcta", "Teoría alternativa", "Hipótesis descartada", "Dato incorrecto"]
                
        elif tema == 'historia':
            question_lower = question.lower()
            if 'independencia de méxico' in question_lower or 'independencia de mexico' in question_lower:
                return ["1810", "1821", "1800", "1830"]
            elif 'revolución francesa' in question_lower or 'revolucion francesa' in question_lower:
                return ["1789", "1776", "1800", "1815"]
            elif 'segunda guerra mundial' in question_lower:
                return ["1939-1945", "1914-1918", "1950-1960", "1930-1940"]
            elif 'benito juárez' in question_lower or 'benito juarez' in question_lower:
                return ["Presidente de México", "Conquistador español", "Revolucionario francés", "Emperador azteca"]
            elif 'miguel hidalgo' in question_lower:
                return ["Padre de la patria mexicana", "Rey de España", "General francés", "Explorador inglés"]
            else:
                return ["Siglo XIX", "Siglo XVIII", "Siglo XX", "Siglo XVII"]
                
        elif tema == 'literatura':
            question_lower = question.lower()
            if 'don quijote' in question_lower:
                return ["Miguel de Cervantes", "García Márquez", "Shakespeare", "Dante"]
            elif 'cien años de soledad' in question_lower:
                return ["Gabriel García Márquez", "Miguel de Cervantes", "Pablo Neruda", "Octavio Paz"]
            elif 'shakespeare' in question_lower:
                return ["Dramaturgo inglés", "Poeta español", "Novelista francés", "Filósofo alemán"]
            elif 'sor juana' in question_lower:
                return ["Poeta novohispana", "Actriz francesa", "Pintora italiana", "Música alemana"]
            else:
                return ["Autor clásico", "Movimiento literario", "Obra contemporánea", "Género narrativo"]
                
        elif tema == 'geografia':
            question_lower = question.lower()
            if 'capital de méxico' in question_lower or 'capital de mexico' in question_lower:
                return ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla"]
            elif 'capital de brasil' in question_lower:
                return ["Brasilia", "São Paulo", "Río de Janeiro", "Salvador"]
            elif 'capital de españa' in question_lower or 'capital de espana' in question_lower:
                return ["Madrid", "Barcelona", "Valencia", "Sevilla"]
            elif 'continente' in question_lower:
                if 'méxico' in question_lower or 'mexico' in question_lower:
                    return ["América", "Europa", "Asia", "África"]
                elif 'brasil' in question_lower:
                    return ["América", "Europa", "Asia", "África"]
                else:
                    return ["América", "Europa", "Asia", "África"]
            elif 'río más largo' in question_lower or 'rio mas largo' in question_lower:
                if 'américa' in question_lower or 'america' in question_lower:
                    return ["Amazonas", "Misisipi", "Río Grande", "Colorado"]
                else:
                    return ["Amazonas", "Nilo", "Yangtsé", "Misisipi"]
            else:
                return ["Norte América", "Sur América", "Europa", "Asia"]
                
        else:
            # Opciones genéricas más variadas
            generic_options = [
                ["Opción correcta A", "Alternativa B", "Posibilidad C", "Variante D"],
                ["Primera respuesta", "Segunda opción", "Tercera alternativa", "Cuarta posibilidad"],
                ["Respuesta A", "Respuesta B", "Respuesta C", "Respuesta D"],
                ["Alternativa 1", "Alternativa 2", "Alternativa 3", "Alternativa 4"]
            ]
            return random.choice(generic_options)

    def _generate_smart_options(self, tema: str, question: str, question_index: int) -> tuple:
        """Genera opciones inteligentes con respuesta correcta distribuida aleatoriamente"""
        opciones_base = self._generate_generic_options(tema, question)
        
        # Asegurar distribución equilibrada de respuestas (A, B, C, D)
        # Usar el índice de la pregunta para evitar patrones predecibles
        respuesta_index = (question_index + random.randint(0, 3)) % 4
        respuesta_letra = chr(65 + respuesta_index)  # A, B, C, D
        
        # Si tenemos opciones inteligentes (específicas del tema), reordenar
        if len(opciones_base) >= 4:
            opciones_final = opciones_base[:4]  # Tomar solo las primeras 4
            # Mezclar opciones para evitar que la primera sea siempre correcta
            random.shuffle(opciones_final)
        else:
            opciones_final = opciones_base + ["Opción adicional"] * (4 - len(opciones_base))
        
        return opciones_final, respuesta_letra

    def _generate_programming_options(self, question: str) -> List[str]:
        """Genera opciones específicas para programación basadas en la pregunta"""
        question_lower = question.lower()
        
        # Detectar conceptos generales de programación primero
        if 'iteración' in question_lower or 'iteracion' in question_lower:
            if 'programación estructurada' in question_lower or 'programacion estructurada' in question_lower:
                return ["Repetición controlada de instrucciones", "Función recursiva", "Variable temporal", "Clase abstracta"]
            else:
                return ["Bucle for", "Bucle while", "Bucle do-while", "Todas las anteriores"]
        
        elif 'patrón' in question_lower or 'patron' in question_lower:
            if 'notificación' in question_lower or 'notificacion' in question_lower:
                return ["Observer", "Singleton", "Factory", "Strategy"]
            elif 'creación' in question_lower or 'creacion' in question_lower:
                return ["Factory", "Observer", "Strategy", "Decorator"]
            else:
                return ["Singleton", "Observer", "Factory", "Strategy"]
        
        # Opciones para diferentes tipos de preguntas de programación por lenguaje
        if 'python' in question_lower:
            if 'función' in question_lower or 'function' in question_lower:
                if 'print' in question_lower:
                    return ["Muestra texto en pantalla", "Declara una variable", "Crea un objeto", "Termina el programa"]
                elif 'len' in question_lower:
                    return ["Devuelve la longitud", "Convierte a texto", "Ordena elementos", "Elimina espacios"]
                elif 'append' in question_lower:
                    return ["Añade elemento al final", "Elimina elementos", "Ordena la lista", "Invierte el orden"]
                elif 'join' in question_lower:
                    return ["Une elementos con separador", "Separa cadenas", "Ordena elementos", "Elimina duplicados"]
                elif 'sort' in question_lower:
                    return ["Ordena los elementos", "Añade elementos", "Busca elementos", "Copia la lista"]
                elif 'split' in question_lower:
                    return ["Divide cadena en lista", "Une elementos", "Ordena texto", "Elimina espacios"]
                elif 'input' in question_lower:
                    return ["Recibe entrada del usuario", "Muestra texto", "Guarda archivo", "Calcula números"]
                elif 'range' in question_lower:
                    return ["Genera secuencia numérica", "Ordena números", "Suma valores", "Cuenta elementos"]
                else:
                    return ["Ejecuta una acción específica", "Declara una variable", "Crea un objeto", "Termina el programa"]
            elif 'tipo de dato' in question_lower:
                return ["String", "Integer", "Boolean", "List"]
            else:
                return ["Python", "JavaScript", "Java", "C++"]
        
        elif 'javascript' in question_lower:
            if 'operador' in question_lower:
                if '++' in question_lower:
                    return ["Incrementa en 1", "Decrementa en 1", "Compara valores", "Asigna valor"]
                elif '--' in question_lower:
                    return ["Decrementa en 1", "Incrementa en 1", "Compara valores", "Asigna valor"]
                elif '==' in question_lower:
                    return ["Compara valores", "Asigna valor", "Incrementa", "Concatena"]
                elif '===' in question_lower:
                    return ["Comparación estricta", "Asignación", "Concatenación", "Incremento"]
                else:
                    return ["Operador de comparación", "Operador aritmético", "Operador lógico", "Operador de asignación"]
            else:
                return ["var", "let", "const", "function"]
        
        elif 'c++' in question_lower or 'cpp' in question_lower:
            if 'operador' in question_lower:
                if '||' in question_lower:
                    return ["OR lógico", "AND lógico", "Asignación", "Comparación"]
                elif '&&' in question_lower:
                    return ["AND lógico", "OR lógico", "Asignación", "Incremento"]
                elif '++'  in question_lower:
                    return ["Incrementa en 1", "Decrementa en 1", "Suma variables", "Declara entero"]
                elif '--' in question_lower:
                    return ["Decrementa en 1", "Incrementa en 1", "Resta variables", "Declara entero"]
                else:
                    return ["Operador lógico", "Operador aritmético", "Operador de comparación", "Operador de asignación"]
            else:
                return ["#include", "int main()", "cout", "cin"]
        
        elif 'java' in question_lower:
            # Manejar comparación específica Java vs C#
            if 'c#' in question_lower and 'diferencia' in question_lower:
                return ["Java es multiplataforma", "C# es más rápido", "Java usa .NET", "C# es interpretado"]
            elif 'public static void main' in question_lower:
                return ["Punto de entrada del programa", "Declara variable global", "Define clase principal", "Importa librerías"]
            if 'tipo de dato' in question_lower:
                if 'replace' in question_lower or 'charAt' in question_lower or 'substring' in question_lower:
                    return ["String", "int", "boolean", "void"]
                else:
                    return ["int", "String", "boolean", "double"]
            else:
                return ["public", "private", "protected", "static"]
        
        elif 'php' in question_lower:
            if 'lambdas' in question_lower or 'lambda' in question_lower:
                return ["function() use($var) {}", "$variable", "var variable", "let variable"]
            elif 'async' in question_lower:
                return ["Con promesas y generators", "No soporta async/await nativo", "Solo con frameworks", "Usando threading"]
            elif 'operador' in question_lower and '--' in question_lower:
                return ["Decrementa en 1", "Incrementa en 1", "Compara valores", "Concatena strings"]
            elif 'sintaxis' in question_lower and 'función' in question_lower:
                return ["function nombreFuncion()", "def nombreFuncion()", "func nombreFuncion()", "void nombreFuncion()"]
            elif 'extends' in question_lower:
                return ["Herencia de clases", "Importar módulos", "Declarar variables", "Crear instancias"]
            else:
                return ["$variable", "variable", "var variable", "let variable"]
        
        elif 'c#' in question_lower:
            if 'tipo de dato' in question_lower and ('charAt' in question_lower or 'string' in question_lower):
                return ["char", "string", "int", "bool"]
            elif 'this' in question_lower:
                return ["Referencia al objeto actual", "Palabra reservada para herencia", "Declara variable estática", "Importa namespace"]
            elif 'super' in question_lower:
                return ["Accede a la clase padre", "Referencia al objeto actual", "Declara método virtual", "Crea nueva instancia"]
            else:
                return ["public", "private", "protected", "internal"]
        
        elif 'algoritmo' in question_lower or 'complejidad' in question_lower:
            if 'búsqueda binaria' in question_lower or 'binary search' in question_lower:
                return ["O(log n)", "O(n)", "O(1)", "O(n²)"]
            elif 'quicksort' in question_lower:
                return ["O(n log n) promedio", "O(n)", "O(log n)", "O(n²) siempre"]
            elif 'mergesort' in question_lower:
                return ["O(n log n)", "O(n)", "O(log n)", "O(n²)"]
            elif 'búsqueda lineal' in question_lower:
                return ["O(n)", "O(log n)", "O(1)", "O(n²)"]
            else:
                return ["O(n log n)", "O(n)", "O(log n)", "O(n²)"]
        
        elif 'patrón' in question_lower or 'design pattern' in question_lower:
            if 'creación de objetos' in question_lower:
                return ["Factory", "Observer", "Strategy", "Decorator"]
            elif 'notificación de cambios' in question_lower:
                return ["Observer", "Singleton", "Factory", "Strategy"]
            elif 'acceso a datos' in question_lower:
                return ["DAO (Data Access Object)", "Singleton", "Observer", "Factory"]
            elif 'estado de objeto' in question_lower:
                return ["State", "Strategy", "Observer", "Factory"]
            else:
                return ["Singleton", "Observer", "Factory", "Strategy"]
        
        elif 'para qué se utiliza' in question_lower or 'para que se utiliza' in question_lower:
            if 'arrays' in question_lower:
                return ["Almacenar múltiples valores del mismo tipo", "Solo para números enteros", "Crear funciones", "Acelerar la red"]
            elif 'listas enlazadas' in question_lower:
                return ["Inserción y eliminación dinámica", "Solo almacenar números", "Crear interfaces gráficas", "Optimizar memoria únicamente"]
            elif 'pilas' in question_lower or 'stack' in question_lower:
                return ["Estructura LIFO para gestión de memoria", "Solo para números", "Crear bases de datos", "Acelerar búsquedas"]
            elif 'colas' in question_lower or 'queue' in question_lower:
                return ["Estructura FIFO para procesos", "Solo almacenar texto", "Crear gráficos", "Optimizar disco"]
            elif 'árboles' in question_lower or 'trees' in question_lower:
                return ["Representar jerarquías y búsquedas rápidas", "Solo para archivos", "Crear redes", "Almacenar imágenes"]
            elif 'grafos' in question_lower or 'graphs' in question_lower:
                return ["Modelar relaciones entre elementos", "Solo para matemáticas", "Crear interfaces", "Almacenar videos"]
            elif 'hash tables' in question_lower:
                return ["Acceso rápido mediante clave-valor", "Solo para texto", "Crear animaciones", "Comprimir archivos"]
            else:
                return ["Organizar y gestionar datos eficientemente", "Solo almacenar números", "Acelerar la red", "Crear interfaces"]
            if 'arrays' in question_lower:
                return ["Acceso directo por índice", "Inserción al final", "Búsqueda secuencial", "Todas las anteriores"]
            elif 'pilas' in question_lower or 'stack' in question_lower:
                return ["Estructura LIFO (Last In, First Out)", "Estructura FIFO", "Acceso aleatorio", "Búsqueda rápida"]
            elif 'colas' in question_lower or 'queue' in question_lower:
                return ["Estructura FIFO (First In, First Out)", "Estructura LIFO", "Acceso aleatorio", "Búsqueda binaria"]
            elif 'árboles' in question_lower or 'trees' in question_lower:
                return ["Jerarquía de nodos", "Estructura lineal", "Acceso secuencial", "Solo para números"]
            elif 'grafos' in question_lower or 'graphs' in question_lower:
                return ["Nodos conectados por aristas", "Solo estructuras lineales", "Para datos ordenados únicamente", "Arrays multidimensionales"]
            else:
                return ["Organizar datos eficientemente", "Solo almacenar números", "Acelerar la red", "Todas las anteriores"]
        
        elif 'diferencia' in question_lower:
            if 'variable' in question_lower and 'constante' in question_lower:
                return ["Las variables pueden cambiar, las constantes no", "Son lo mismo", "Las constantes son más rápidas", "No hay diferencia práctica"]
            elif 'función' in question_lower and 'método' in question_lower:
                return ["Los métodos pertenecen a una clase", "Las funciones son más rápidas", "Son sinónimos exactos", "Los métodos son siempre privados"]
            elif 'python' in question_lower:
                if 'javascript' in question_lower:
                    return ["Python es interpretado, JS puede ser compilado JIT", "Son idénticos", "Python es más rápido", "JS no soporta OOP"]
                elif 'java' in question_lower:
                    return ["Python es dinámico, Java es estático", "Son el mismo lenguaje", "Python es compilado", "Java es interpretado"]
                elif 'php' in question_lower:
                    return ["Python es uso general, PHP es web", "Son idénticos", "PHP es más rápido", "Python no soporta web"]
                elif 'c++' in question_lower:
                    return ["Python es interpretado, C++ es compilado", "Son idénticos", "Python es más rápido", "C++ es interpretado"]
                elif 'ruby' in question_lower:
                    return ["Python es más popular, Ruby es más elegante", "Son idénticos", "Python es compilado", "Ruby no soporta OOP"]
                elif 'r' in question_lower:
                    return ["Python es uso general, R es estadístico", "Son idénticos", "Python es más lento", "R es mejor para web"]
                else:
                    return ["Diferentes paradigmas", "Distintas sintaxis", "Diferentes propósitos", "Todas las anteriores"]
            else:
                return ["Sintaxis diferente", "Propósito diferente", "Rendimiento diferente", "Todas las anteriores"]
        
        elif 'ventaja' in question_lower:
            if 'vue.js' in question_lower and 'express' in question_lower:
                return ["Vue.js es frontend, Express.js es backend", "Vue.js es más rápido", "Vue.js tiene mejor SEO", "Son equivalentes"]
            elif 'react' in question_lower:
                return ["Virtual DOM y componentes reutilizables", "Mejor SEO automático", "Más rápido que HTML puro", "Solo para móviles"]
            elif 'angular' in question_lower:
                return ["Framework completo con TypeScript", "Solo para SPAs", "Más simple que React", "No necesita JavaScript"]
            elif 'django' in question_lower:
                return ["Framework completo con ORM", "Solo para APIs", "No soporta bases de datos", "Solo para principiantes"]
            elif 'flask' in question_lower:
                return ["Ligero y flexible", "Más complejo que Django", "Solo para APIs REST", "No soporta templates"]
            else:
                return ["Mayor eficiencia", "Mejor mantenibilidad", "Más escalabilidad", "Todas las anteriores"]
        
        elif 'implementa' in question_lower:
            if 'async/await' in question_lower:
                return ["Con promesas nativas", "Solo con librerías externas", "No es posible", "Solo en funciones estáticas"]
            elif 'herencia múltiple' in question_lower:
                return ["Con interfaces y mixins", "Nativamente como C++", "No es posible", "Solo con decoradores"]
            elif 'generators' in question_lower:
                return ["Con yield y función generadora", "Solo con arrays", "No soportado", "Solo con async"]
            else:
                return ["Con sintaxis específica", "No es posible", "Solo con librerías", "Automáticamente"]
        
        elif 'sintaxis' in question_lower and 'correcta' in question_lower:
            if 'clase' in question_lower:
                if 'python' in question_lower:
                    return ["class NombreClase:", "def NombreClase:", "class NombreClase()", "new NombreClase"]
                elif 'java' in question_lower:
                    return ["class NombreClase {}", "public class NombreClase", "class NombreClase() {}", "new class NombreClase"]
                elif 'javascript' in question_lower:
                    return ["class NombreClase {}", "function NombreClase()", "var NombreClase = class", "Todas las anteriores"]
                elif 'ruby' in question_lower:
                    return ["class NombreClase", "def class NombreClase", "class NombreClase()", "new class NombreClase"]
                elif 'c++' in question_lower:
                    return ["class NombreClase {};", "public class NombreClase", "class NombreClase() {}", "new class NombreClase"]
                else:
                    return ["class NombreClase", "def NombreClase", "function NombreClase", "new NombreClase"]
            elif 'función' in question_lower:
                if 'python' in question_lower:
                    return ["def nombre_funcion():", "function nombre_funcion()", "func nombre_funcion()", "void nombre_funcion()"]
                elif 'javascript' in question_lower:
                    return ["function nombre_funcion()", "def nombre_funcion()", "func nombre_funcion()", "void nombre_funcion()"]
                elif 'php' in question_lower:
                    return ["function nombreFuncion()", "def nombreFuncion()", "func nombreFuncion()", "void nombreFuncion()"]
                else:
                    return ["Depende del lenguaje", "function nombre()", "def nombre()", "Todas son válidas"]
            elif 'variable' in question_lower:
                if 'python' in question_lower:
                    return ["variable = valor", "var variable = valor", "let variable = valor", "$variable = valor"]
                elif 'javascript' in question_lower:
                    return ["let variable = valor", "variable = valor", "$variable = valor", "def variable = valor"]
                elif 'php' in question_lower:
                    return ["$variable = valor", "variable = valor", "let variable = valor", "def variable = valor"]
                else:
                    return ["Depende del lenguaje", "variable = valor", "$variable = valor", "let variable = valor"]
            elif 'bucle for' in question_lower:
                if 'python' in question_lower:
                    return ["for i in range():", "for (i = 0; i < n; i++)", "foreach i in array", "for i to n"]
                elif 'javascript' in question_lower:
                    return ["for (let i = 0; i < n; i++)", "for i in range()", "foreach i in array", "for i to n"]
                elif 'java' in question_lower:
                    return ["for (int i = 0; i < n; i++)", "for i in range()", "foreach i in array", "for i to n"]
                else:
                    return ["Depende del lenguaje", "for (i = 0; i < n; i++)", "for i in range()", "Todas son válidas"]
            else:
                return ["Depende del lenguaje específico", "Sintaxis estándar", "No hay sintaxis correcta", "Todas son válidas"]
        
        elif 'propósito' in question_lower or 'proposito' in question_lower:
            if 'this' in question_lower:
                return ["Referencia al objeto actual", "Palabra reservada para herencia", "Declara variable estática", "Importa namespace"]
            elif 'super' in question_lower:
                return ["Accede a la clase padre", "Referencia al objeto actual", "Declara método virtual", "Crea nueva instancia"]
            elif 'static' in question_lower:
                return ["Pertenece a la clase, no a instancias", "Variable que no cambia", "Método privado", "Importa bibliotecas"]
            elif 'final' in question_lower:
                return ["No puede ser modificado/heredado", "Última función ejecutada", "Variable temporal", "Método público"]
            elif 'abstract' in question_lower:
                return ["Define estructura sin implementación", "Variable abstracta", "Función matemática", "Importa módulos"]
            elif 'extends' in question_lower:
                return ["Herencia de clases", "Importar módulos", "Declarar variables", "Crear instancias"]
            elif 'interface' in question_lower:
                return ["Contrato que deben cumplir las clases", "Interfaz gráfica", "Conexión de red", "Base de datos"]
            else:
                return ["Define comportamiento específico", "Optimiza rendimiento", "Gestiona memoria", "Todas las anteriores"]
        
        elif 'significa' in question_lower or 'qué es' in question_lower:
            if 'recursión' in question_lower or 'recursion' in question_lower:
                return ["Función que se llama a sí misma", "Bucle infinito", "Función sin parámetros", "Variable global"]
            elif 'iteración' in question_lower or 'iteracion' in question_lower:
                return ["Repetición controlada de instrucciones", "Función recursiva", "Variable temporal", "Clase abstracta"]
            elif 'polimorfismo' in question_lower:
                return ["Múltiples formas para un mismo método", "Herencia múltiple", "Variables dinámicas", "Compilación automática"]
            elif 'herencia' in question_lower:
                if 'estructurada' in question_lower:
                    return ["No aplica en programación estructurada", "Jerarquía de funciones", "Variables compartidas", "Módulos interconectados"]
                else:
                    return ["Clase que adquiere propiedades de otra", "Copia de código", "Variables compartidas", "Funciones globales"]
            elif 'encapsulación' in question_lower or 'encapsulacion' in question_lower:
                return ["Ocultar detalles internos de implementación", "Dividir código en archivos", "Usar variables privadas únicamente", "Compilar código automáticamente"]
            elif 'abstracción' in question_lower or 'abstraccion' in question_lower:
                return ["Simplificar conceptos complejos", "Usar funciones abstractas únicamente", "Evitar herencia", "Optimizar rendimiento"]
            elif 'framework' in question_lower:
                return ["Estructura base para desarrollar aplicaciones", "Lenguaje de programación", "Base de datos", "Sistema operativo"]
            elif 'api' in question_lower:
                return ["Interfaz para comunicar aplicaciones", "Base de datos", "Lenguaje de programación", "Sistema de archivos"]
            elif 'git' in question_lower:
                return ["Sistema de control de versiones", "Editor de código", "Base de datos", "Framework web"]
            elif 'debugging' in question_lower:
                return ["Proceso de encontrar y corregir errores", "Optimizar rendimiento", "Compilar código", "Crear documentación"]
            else:
                return ["Concepto fundamental en programación", "Función especial", "Variable especial", "Todas las anteriores"]
        
        elif 'range' in question_lower and 'función' in question_lower:
            if 'python' in question_lower:
                return ["Genera secuencia numérica", "Ordena números", "Suma valores", "Cuenta elementos"]
            elif 'php' in question_lower:
                return ["PHP no tiene función range() nativa", "Genera arrays", "Ordena arrays", "Cuenta elementos"]
            elif 'javascript' in question_lower:
                return ["No existe función range() nativa", "Genera arrays", "Itera elementos", "Ordena números"]
            else:
                return ["Genera secuencia numérica", "Ordena elementos", "Suma valores", "Cuenta elementos"]
        
        elif 'maneja' in question_lower and 'error' in question_lower:
            if 'memory leaks' in question_lower:
                return ["Gestión automática de memoria y buenas prácticas", "Solo con librerías externas", "No es posible prevenir", "Solo en lenguajes compilados"]
            elif 'excepciones' in question_lower:
                return ["try-catch-finally", "if-else únicamente", "switch-case", "Solo con logs"]
            elif 'sintaxis' in question_lower:
                return ["IDE y linters en tiempo real", "Solo en tiempo de ejecución", "No se pueden detectar", "Solo con pruebas unitarias"]
            else:
                return ["Con bloques try-catch", "Solo con if-else", "Ignorándolos", "Con switch-case"]
        
        # Opciones por defecto mejoradas y más específicas para programación
        # Analizar la pregunta para dar opciones contextualmente apropiadas
        if any(word in question_lower for word in ['función', 'funcion', 'method', 'método']):
            return ["Ejecuta una operación específica", "Declara una variable global", "Crea un objeto nuevo", "Termina el programa"]
        elif any(word in question_lower for word in ['variable', 'constante', 'dato']):
            return ["Almacena y manipula información", "Solo para números enteros", "Controla el flujo del programa", "Optimiza la memoria"]
        elif any(word in question_lower for word in ['clase', 'objeto', 'instancia']):
            return ["Define estructura y comportamiento", "Solo para matemáticas", "Acelera la ejecución", "Maneja errores"]
        elif any(word in question_lower for word in ['algoritmo', 'complejidad', 'eficiencia']):
            return ["Optimiza tiempo y recursos", "Solo para ordenar datos", "Mejora la interfaz", "Reduce el código"]
        elif any(word in question_lower for word in ['herencia', 'polimorfismo', 'encapsulación']):
            return ["Principio de programación orientada a objetos", "Función matemática", "Comando de terminal", "Tipo de variable"]
        elif any(word in question_lower for word in ['framework', 'biblioteca', 'library']):
            return ["Facilita el desarrollo de aplicaciones", "Solo para diseño web", "Optimiza la base de datos", "Acelera la red"]
        elif any(word in question_lower for word in ['debugging', 'depuración', 'error']):
            return ["Proceso de encontrar y corregir errores", "Optimizar el rendimiento", "Crear documentación", "Diseñar interfaces"]
        elif any(word in question_lower for word in ['sintaxis', 'código', 'programar']):
            return ["Reglas del lenguaje de programación", "Solo para principiantes", "Optimiza la memoria", "Acelera la compilación"]
        else:
            return ["Concepto fundamental de programación", "Técnica avanzada de optimización", "Herramienta de desarrollo", "Estándar de la industria"]

    def _parse_ollama_response(self, text: str, tipo_examen: str) -> List[Dict]:
        """Parsea la respuesta de Ollama"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        questions = []
        
        for line in lines[:10]:  # Máximo 10 preguntas
            if tipo_examen == 'opciones':
                # Formato esperado: pregunta|opcionA|opcionB|opcionC|opcionD|respuesta
                parts = line.split('|')
                if len(parts) >= 6:
                    questions.append({
                        'pregunta': parts[0],
                        'opciones': parts[1:5],
                        'respuesta': parts[5]
                    })
            else:
                questions.append(line)
        
        return questions

    def generate_exam(self, tema: str, cantidad: int, tipo_examen: str = 'simple', method: str = 'offline') -> List[Dict]:
        """Método principal para generar exámenes"""
        if method == 'ollama':
            return self.generate_with_ollama(tema, cantidad, tipo_examen)
        elif method == 'huggingface':
            return self.generate_with_huggingface(tema, cantidad, tipo_examen)
        else:
            return self.generate_offline(tema, cantidad, tipo_examen)

# Función de utilidad para usar en Flask
def generate_local_exam(tema: str, cantidad: int, tipo_examen: str = 'simple', method: str = 'offline'):
    """Función simplificada para usar en la aplicación Flask"""
    generator = LocalAIExamGenerator()
    return generator.generate_exam(tema, cantidad, tipo_examen, method)

if __name__ == "__main__":
    # Prueba del generador
    generator = LocalAIExamGenerator()
    
    print("=== Prueba Generador Offline - Programación ===")
    questions = generator.generate_offline("programación", 5, "opciones")
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q['pregunta']}")
        if 'opciones' in q:
            for j, opt in enumerate(q['opciones']):
                print(f"   {chr(65+j)}) {opt}")
            print(f"   Respuesta correcta: {q['respuesta']}")
        else:
            print(f"   Respuesta: {q}")
    
    print("\n=== Prueba Generador Simple - Programación ===")
    questions = generator.generate_offline("programación", 3, "simple")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    
    print("\n=== Prueba Generador Offline - Matemáticas ===")
    questions = generator.generate_offline("matemáticas", 3, "opciones")
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q['pregunta']}")
        if 'opciones' in q:
            for j, opt in enumerate(q['opciones']):
                print(f"   {chr(65+j)}) {opt}")
            print(f"   Respuesta correcta: {q['respuesta']}")
    
    print("\n=== Prueba con tema no reconocido ===")
    questions = generator.generate_offline("tema_inventado", 2, "opciones")
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q['pregunta']}")
        if 'opciones' in q:
            for j, opt in enumerate(q['opciones']):
                print(f"   {chr(65+j)}) {opt}")
            print(f"   Respuesta correcta: {q['respuesta']}")