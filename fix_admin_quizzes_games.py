from models import db, User, Quiz, Game
from app import app

with app.app_context():
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        print("No se encontró usuario admin.")
        exit(1)
    # Actualizar quizzes: teacher_id a None si los creó el admin
    quizzes = Quiz.query.filter((Quiz.teacher_id != None) & (Quiz.created_by == admin.id)).all()
    for q in quizzes:
        q.teacher_id = None
        print(f"Quiz actualizado: {q.title}")
    # Actualizar juegos: teacher_id a None si teacher_id no es None (solo los juegos sin profesor)
    games = Game.query.filter(Game.teacher_id != None).all()
    for g in games:
        g.teacher_id = None
        print(f"Juego actualizado: {g.name}")
    db.session.commit()
    print("Actualización completada.")
