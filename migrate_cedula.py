"""
Script de migración para agregar campos de cédula profesional
Ejecutar este script para actualizar la base de datos sin perder datos existentes
"""

from app import app, db
from models import Teacher
from sqlalchemy import text

def migrate_cedula_fields():
    with app.app_context():
        try:
            # Intentar agregar las columnas si no existen
            with db.engine.connect() as conn:
                # Para PostgreSQL
                try:
                    conn.execute(text("""
                        ALTER TABLE teachers
                        ADD COLUMN IF NOT EXISTS cedula_profesional_img VARCHAR(300)
                    """))
                    conn.execute(text("""
                        ALTER TABLE teachers
                        ADD COLUMN IF NOT EXISTS cedula_verified BOOLEAN DEFAULT FALSE
                    """))
                    conn.commit()
                    print("✅ Migración completada exitosamente (PostgreSQL)")
                except Exception as e:
                    # Para SQLite u otras bases de datos
                    conn.rollback()
                    try:
                        # Verificar si la columna ya existe
                        result = conn.execute(text("PRAGMA table_info(teachers)"))
                        columns = [row[1] for row in result]

                        if 'cedula_profesional_img' not in columns:
                            conn.execute(text("""
                                ALTER TABLE teachers
                                ADD COLUMN cedula_profesional_img VARCHAR(300)
                            """))
                            print("✅ Columna cedula_profesional_img agregada")
                        else:
                            print("ℹ️  Columna cedula_profesional_img ya existe")

                        if 'cedula_verified' not in columns:
                            conn.execute(text("""
                                ALTER TABLE teachers
                                ADD COLUMN cedula_verified BOOLEAN DEFAULT 0
                            """))
                            print("✅ Columna cedula_verified agregada")
                        else:
                            print("ℹ️  Columna cedula_verified ya existe")

                        conn.commit()
                        print("✅ Migración completada exitosamente (SQLite)")
                    except Exception as e2:
                        print(f"❌ Error en la migración: {e2}")
                        conn.rollback()
                        raise

            print("\n📊 Resumen de la migración:")
            print("   - Campo 'cedula_profesional_img' para almacenar la ruta de la imagen")
            print("   - Campo 'cedula_verified' para el estado de verificación")
            print("\n✨ La base de datos está lista para usar la funcionalidad de cédula profesional")

        except Exception as e:
            print(f"❌ Error fatal en la migración: {e}")
            raise

if __name__ == '__main__':
    print("🔄 Iniciando migración de base de datos...")
    print("   Agregando campos para cédula profesional...")
    migrate_cedula_fields()
