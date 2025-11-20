import os
from dotenv import load_dotenv

# Cargar variables desde .env en entorno local (Railway ya inyecta env vars en producción)
load_dotenv()

# Normalizar URL de PostgreSQL (Railway a veces entrega postgres://)
_raw_db_url = os.environ.get('DATABASE_URL')
if _raw_db_url and _raw_db_url.startswith('postgres://'):
	_raw_db_url = _raw_db_url.replace('postgres://', 'postgresql://', 1)

# Configuración de base de datos - usar SQLite por defecto si no hay DATABASE_URL
SQLALCHEMY_DATABASE_URI = _raw_db_url or 'sqlite:///mentora.db'

# Clave secreta - usar variable de entorno en producción
SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_super_secreta_para_mentora'
