"""
Script de migración para agregar columnas faltantes a la tabla teachers
"""
import os
import sys
from sqlalchemy import text

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_teacher_table():
    """Agrega las columnas faltantes a la tabla teachers si no existen"""
    with app.app_context():
        try:
            # Verificar si la columna cedula_profesional_img existe
            check_column = text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='teachers'
                AND column_name='cedula_profesional_img'
            """)

            result = db.session.execute(check_column).fetchone()

            if result is None:
                print("📝 Agregando columna 'cedula_profesional_img' a la tabla teachers...")
                alter_table = text("""
                    ALTER TABLE teachers
                    ADD COLUMN cedula_profesional_img VARCHAR(300),
                    ADD COLUMN cedula_verified BOOLEAN DEFAULT FALSE
                """)
                db.session.execute(alter_table)
                db.session.commit()
                print("✅ Columnas agregadas exitosamente!")
            else:
                print("✅ Las columnas ya existen en la tabla teachers")

        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    print("🚀 Iniciando migración de la tabla teachers...")
    migrate_teacher_table()
    print("🎉 Migración completada!")
