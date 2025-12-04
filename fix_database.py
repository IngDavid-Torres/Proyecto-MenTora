"""
Script simple para agregar columnas a la base de datos
"""
import sqlite3
import os

# Ruta a la base de datos
db_path = 'instance/mentora.db'

if not os.path.exists(db_path):
    print(f"Error: No se encuentra la base de datos en {db_path}")
    exit(1)

# Conectar a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Intentar agregar la columna cedula_profesional_img
    try:
        cursor.execute("ALTER TABLE teachers ADD COLUMN cedula_profesional_img VARCHAR(300)")
        print("Columna cedula_profesional_img agregada exitosamente")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Columna cedula_profesional_img ya existe")
        else:
            raise

    # Intentar agregar la columna cedula_verified
    try:
        cursor.execute("ALTER TABLE teachers ADD COLUMN cedula_verified BOOLEAN DEFAULT 0")
        print("Columna cedula_verified agregada exitosamente")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Columna cedula_verified ya existe")
        else:
            raise

    # Guardar cambios
    conn.commit()
    print("\nMigracion completada exitosamente!")
    print("Las columnas han sido agregadas a la tabla teachers")

except Exception as e:
    print(f"Error durante la migracion: {e}")
    conn.rollback()

finally:
    conn.close()
