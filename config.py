import os
from dotenv import load_dotenv

# Cargar variables desde .env en entorno local (Railway ya inyecta env vars en producción)
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Clave secreta - usar variable de entorno siempre
SECRET_KEY = os.environ.get('SECRET_KEY')
