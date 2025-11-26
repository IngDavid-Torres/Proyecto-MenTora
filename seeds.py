"""Script de seed para MenTora.
Ejecuta datos iniciales (idempotente) sin duplicar registros.

Uso local:
    python seeds.py

En Railway (opcional):
    Añade variable SEED_ON_DEPLOY=1 y llama desde railway.sh antes de gunicorn.

NOTA: Para migraciones reales usa Flask-Migrate; esto es sólo datos iniciales.
"""

from flask import Flask
from werkzeug.security import generate_password_hash
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from models import db, User, Teacher, Badge, Quiz, Question

# Crear app mínima para seeding (evita efectos secundarios de importar app completa)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)


def get_or_create(model, defaults=None, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    params = dict(kwargs)
    if defaults:
        params.update(defaults)
    instance = model(**params)
    db.session.add(instance)
    return instance, True


def seed_admin_and_teacher():
    import os
    admin_password = os.environ.get('ADMIN_PASSWORD', 'MenToraAdmin123')
    prof_password = os.environ.get('PROF_PASSWORD', 'MenToraProf123')
    admin, created = get_or_create(User, username="admin")
    if created:
        admin.email = "admin@mentora.com"
        admin.password = generate_password_hash(admin_password)
        admin.area = "general"
        admin.is_admin = True
        admin.points = 0
        admin.level = 1
    teacher_user, created_t = get_or_create(User, username="prof_demo")
    if created_t:
        teacher_user.email = "prof_demo@mentora.com"
        teacher_user.password = generate_password_hash(prof_password)
        teacher_user.area = "programacion"
        teacher_user.is_admin = False
        teacher_user.points = 0
        teacher_user.level = 1
    if not getattr(teacher_user, "teacher_profile", None):
        get_or_create(Teacher, user_id=teacher_user.id)
    return admin, teacher_user


def seed_badges():
    badge_defs = [
        ("Primer Quiz", "Completó su primer quiz", "https://example.com/badge1.png"),
        ("5 Quizzes", "Cinco quizzes completados", "https://example.com/badge5.png"),
        ("Experto Área", "Más de 100 puntos en un área", "https://example.com/badge_expert.png")
    ]
    for name, desc, img in badge_defs:
        get_or_create(Badge, name=name, defaults={"description": desc, "image_url": img})


def seed_quizzes_and_questions(teacher_user):
    quiz_defs = [
        {
            "title": "Intro Python",
            "area": "programacion",
            "description": "Conceptos básicos de Python",
            "questions": [
                {
                    "text": "¿Qué palabra clave define una función?",
                    "options": ["def", "function", "fn", "lambda"],
                    "correct": "def"
                },
                {
                    "text": "Tipo de dato de 3.14",
                    "options": ["int", "float", "str", "double"],
                    "correct": "float"
                }
            ]
        },
        {
            "title": "Bases SQL",
            "area": "programacion",
            "description": "Consultas básicas SQL",
            "questions": [
                {
                    "text": "Comando para seleccionar datos",
                    "options": ["GET", "SELECT", "CHOOSE", "FETCH"],
                    "correct": "SELECT"
                }
            ]
        }
    ]
    for qd in quiz_defs:
        quiz, created = get_or_create(Quiz, title=qd["title"], defaults={
            "area": qd["area"],
            "description": qd["description"],
            "created_by": teacher_user.id,
            "teacher_id": getattr(teacher_user, "teacher_profile", None).id if getattr(teacher_user, "teacher_profile", None) else None
        })
        if created:
            for q in qd["questions"]:
                get_or_create(Question, quiz_id=quiz.id, text=q["text"], defaults={
                    "options": q["options"],
                    "correct_answer": q["correct"]
                })


def run_seed():
    with app.app_context():
        db.create_all()
        admin, teacher_user = seed_admin_and_teacher()
        seed_badges()
        seed_quizzes_and_questions(teacher_user)
        db.session.commit()
        print("Seed completado.")


if __name__ == "__main__":
    run_seed()
