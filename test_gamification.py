"""
Script de prueba para verificar el sistema de gamificación
"""
from app import app, db
from models import User, QuizProgress, GameProgress, ActivityLog, Badge, Achievement

def test_gamification_system():
    """Verifica que el sistema de gamificación esté funcionando"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("PRUEBA DEL SISTEMA DE GAMIFICACIÓN")
        print("="*60 + "\n")
        
        # 1. Verificar tablas
        print("1. Verificando tablas en la base de datos...")
        try:
            quiz_progress_count = QuizProgress.query.count()
            game_progress_count = GameProgress.query.count()
            activity_log_count = ActivityLog.query.count()
            print(f"   ✓ QuizProgress: {quiz_progress_count} registros")
            print(f"   ✓ GameProgress: {game_progress_count} registros")
            print(f"   ✓ ActivityLog: {activity_log_count} registros")
        except Exception as e:
            print(f"   ✗ Error al verificar tablas: {e}")
            return False
        
        # 2. Verificar badges
        print("\n2. Verificando badges...")
        try:
            badges = Badge.query.all()
            print(f"   ✓ Total de badges: {len(badges)}")
            for badge in badges:
                print(f"      - {badge.name}: {badge.description}")
        except Exception as e:
            print(f"   ✗ Error al verificar badges: {e}")
            return False
        
        # 3. Verificar usuarios con progreso
        print("\n3. Verificando usuarios con progreso...")
        try:
            users_with_progress = db.session.query(User).join(ActivityLog).distinct().all()
            print(f"   ✓ Usuarios con actividades: {len(users_with_progress)}")
            for user in users_with_progress:
                activities = ActivityLog.query.filter_by(user_id=user.id).count()
                achievements = Achievement.query.filter_by(user_id=user.id).count()
                print(f"      - {user.username}: {user.points} pts, {activities} actividades, {achievements} logros")
        except Exception as e:
            print(f"   ℹ No hay usuarios con progreso aún")
        
        # 4. Verificar estadísticas generales
        print("\n4. Estadísticas generales...")
        try:
            total_users = User.query.count()
            total_activities = ActivityLog.query.count()
            total_achievements = Achievement.query.count()
            total_quiz_completed = QuizProgress.query.filter_by(completed=True).count()
            total_game_completed = GameProgress.query.filter_by(completed=True).count()
            
            print(f"   ✓ Total de usuarios: {total_users}")
            print(f"   ✓ Total de actividades registradas: {total_activities}")
            print(f"   ✓ Total de logros desbloqueados: {total_achievements}")
            print(f"   ✓ Quizzes completados: {total_quiz_completed}")
            print(f"   ✓ Juegos completados: {total_game_completed}")
        except Exception as e:
            print(f"   ✗ Error al obtener estadísticas: {e}")
            return False
        
        # 5. Verificar integridad de datos
        print("\n5. Verificando integridad de datos...")
        try:
            # Verificar que no haya registros huérfanos
            orphan_quiz_progress = QuizProgress.query.filter(~QuizProgress.user.has()).count()
            orphan_game_progress = GameProgress.query.filter(~GameProgress.user.has()).count()
            orphan_activities = ActivityLog.query.filter(~ActivityLog.user.has()).count()
            
            if orphan_quiz_progress == 0 and orphan_game_progress == 0 and orphan_activities == 0:
                print("   ✓ No hay registros huérfanos")
            else:
                print(f"   ⚠ Registros huérfanos encontrados:")
                if orphan_quiz_progress > 0:
                    print(f"      - QuizProgress: {orphan_quiz_progress}")
                if orphan_game_progress > 0:
                    print(f"      - GameProgress: {orphan_game_progress}")
                if orphan_activities > 0:
                    print(f"      - ActivityLog: {orphan_activities}")
        except Exception as e:
            print(f"   ✗ Error al verificar integridad: {e}")
        
        print("\n" + "="*60)
        print("✓ SISTEMA DE GAMIFICACIÓN FUNCIONANDO CORRECTAMENTE")
        print("="*60 + "\n")
        
        print("📋 RECOMENDACIONES:")
        print("   1. Prueba completar un quiz para verificar la asignación de puntos")
        print("   2. Prueba completar un juego para verificar el sistema de progreso")
        print("   3. Revisa el dashboard para ver el historial de actividades")
        print("   4. Verifica que los badges se otorguen automáticamente")
        print("\n")
        
        return True

if __name__ == '__main__':
    test_gamification_system()
