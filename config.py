import os

# Configuración de base de datos - usar SQLite por defecto, PostgreSQL en producción
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mentora.db'

# Clave secreta - usar variable de entorno en producción
SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_super_secreta_para_mentora'