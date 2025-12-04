"""
Script de migracion para agregar columnas faltantes a la tabla teachers
"""
import os
import sys
from sqlalchemy import text

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

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
                print("📝 Agregando columnas a la tabla teachers...")

                # Agregar las columnas una por una para mejor compatibilidad
                try:
                    db.session.execute(text("""
                        ALTER TABLE teachers
                        ADD COLUMN IF NOT EXISTS cedula_profesional_img VARCHAR(300)
                    """))
                    print("  ✓ Columna 'cedula_profesional_img' agregada")
                except Exception as e:
                    print(f"  ⚠ cedula_profesional_img: {e}")

                try:
                    db.session.execute(text("""
                        ALTER TABLE teachers
                        ADD COLUMN IF NOT EXISTS cedula_verified BOOLEAN DEFAULT FALSE
                    """))
                    print("  ✓ Columna 'cedula_verified' agregada")
                except Exception as e:
                    print(f"  ⚠ cedula_verified: {e}")

                db.session.commit()
                print("✅ Migración completada!")
            else:
                print("✅ Las columnas ya existen en la tabla teachers")

        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            print(f"   Traceback: {e}")
            db.session.rollback()

            # Intentar método alternativo sin IF NOT EXISTS (para PostgreSQL antiguo)
            print("\n🔄 Intentando método alternativo...")
            try:
                db.session.execute(text("""
                    ALTER TABLE teachers
                    ADD COLUMN cedula_profesional_img VARCHAR(300)
                """))
                print("  ✓ Columna 'cedula_profesional_img' agregada")
            except Exception as e2:
                print(f"  ⚠ Ya existe o error: {e2}")

            try:
                db.session.execute(text("""
                    ALTER TABLE teachers
                    ADD COLUMN cedula_verified BOOLEAN DEFAULT FALSE
                """))
                print("  ✓ Columna 'cedula_verified' agregada")
            except Exception as e2:
                print(f"  ⚠ Ya existe o error: {e2}")

            try:
                db.session.commit()
                print("✅ Migración alternativa completada!")
            except Exception as e3:
                print(f"❌ Error en commit: {e3}")
                db.session.rollback()

if __name__ == "__main__":
    print("🚀 Iniciando migración de la tabla teachers...")
    migrate_teacher_table()
    print("🎉 Proceso finalizado!")
