"""
Script para crear las tablas de progreso de gamificación
"""
from app import app, db
from models import QuizProgress, GameProgress, ActivityLog

def create_gamification_tables():
    """Crea las tablas de progreso y actividades si no existen"""
    
    with app.app_context():
        try:
            # Crear todas las tablas definidas en los modelos
            db.create_all()
            print("✓ Tablas de gamificación creadas correctamente:")
            print("  - quiz_progress")
            print("  - game_progress")
            print("  - activity_logs")
            
        except Exception as e:
            print(f"✗ Error al crear tablas: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_gamification_tables()
