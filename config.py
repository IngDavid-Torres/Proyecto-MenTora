import os
from dotenv import load_dotenv
from pathlib import Path

# Obtener la ruta del directorio actual
basedir = Path(__file__).parent

# Cargar variables desde .env en entorno local (Railway ya inyecta env vars en producción)
env_file = basedir / '.env'
load_dotenv(env_file)

# Obtener DATABASE_URL con fallback a SQLite local si no existe
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
if not SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir / "mentora.db"}'

# Clave secreta - usar variable de entorno con fallback
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
