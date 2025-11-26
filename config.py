import os
from dotenv import load_dotenv

# Cargar variables desde .env en entorno local (Railway ya inyecta env vars en producción)
load_dotenv()

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:IaEGobhbIIZPPncNDFbTxponPcaKepKS@shuttle.proxy.rlwy.net:34852/railway'

# Clave secreta - usar variable de entorno en producción
SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_super_secreta_para_mentora'
