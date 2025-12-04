"""
Script para migrar avatares de identicon a notionists
Ejecutar una sola vez para actualizar todos los usuarios existentes
"""
import sys
import io

# Configurar la salida para UTF-8 en Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app import app, db
from models import User

def migrate_avatars():
    with app.app_context():
        # Obtener todos los usuarios que tienen avatares con identicon
        users = User.query.filter(User.avatar_url.like('%identicon%')).all()

        count = 0
        for user in users:
            # Reemplazar identicon por notionists en la URL
            if user.avatar_url and 'identicon' in user.avatar_url:
                user.avatar_url = user.avatar_url.replace('identicon', 'notionists')
                count += 1
                print(f"OK - Actualizado avatar de {user.username}")

        # Guardar cambios
        db.session.commit()
        print(f"\nOK - Migracion completada: {count} avatares actualizados")

if __name__ == '__main__':
    print("Iniciando migracion de avatares...")
    migrate_avatars()
