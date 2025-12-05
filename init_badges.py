"""
Script para inicializar los badges (logros) en la base de datos
"""
from app import app, db
from models import Badge

def init_badges():
    """Crea los badges iniciales si no existen"""
    
    badges_data = [
        {
            'name': 'Primer Quiz',
            'description': 'Completaste tu primer quiz',
            'image_url': '/static/img/badges/primer_quiz.png'
        },
        {
            'name': 'Maestro de Quizzes',
            'description': 'Completaste 5 quizzes',
            'image_url': '/static/img/badges/maestro_quizzes.png'
        },
        {
            'name': 'Primer Juego',
            'description': 'Completaste tu primer juego',
            'image_url': '/static/img/badges/primer_juego.png'
        },
        {
            'name': 'Jugador Experto',
            'description': 'Completaste 5 juegos',
            'image_url': '/static/img/badges/jugador_experto.png'
        },
        {
            'name': '100 Puntos',
            'description': 'Alcanzaste 100 puntos',
            'image_url': '/static/img/badges/100_puntos.png'
        },
        {
            'name': '500 Puntos',
            'description': 'Alcanzaste 500 puntos',
            'image_url': '/static/img/badges/500_puntos.png'
        },
        {
            'name': 'Nivel 5',
            'description': 'Alcanzaste el nivel 5',
            'image_url': '/static/img/badges/nivel_5.png'
        },
        {
            'name': 'Explorador',
            'description': 'Completaste 10 actividades diferentes',
            'image_url': '/static/img/badges/explorador.png'
        },
        {
            'name': 'Dedicado',
            'description': 'Completaste actividades durante 7 días seguidos',
            'image_url': '/static/img/badges/dedicado.png'
        },
        {
            'name': 'Maestro MenTora',
            'description': 'Alcanzaste el nivel 10',
            'image_url': '/static/img/badges/maestro_mentora.png'
        }
    ]
    
    with app.app_context():
        for badge_data in badges_data:
            # Verificar si el badge ya existe
            existing_badge = Badge.query.filter_by(name=badge_data['name']).first()
            if not existing_badge:
                badge = Badge(
                    name=badge_data['name'],
                    description=badge_data['description'],
                    image_url=badge_data['image_url']
                )
                db.session.add(badge)
                print(f"✓ Badge creado: {badge_data['name']}")
            else:
                print(f"- Badge ya existe: {badge_data['name']}")
        
        db.session.commit()
        print("\n✓ Badges inicializados correctamente")

if __name__ == '__main__':
    init_badges()
