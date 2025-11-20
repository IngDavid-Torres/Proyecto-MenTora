#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Build MenTora (instalando dependencias)"
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencias listas"

echo "🗄️ Asegurando tablas de base de datos"
python - <<'PYCODE'
from app import app
from models import db
with app.app_context():
	db.create_all()
	print("Tablas OK")
PYCODE

echo "🔥 Lanzando servidor Gunicorn + Eventlet"
WORKERS="${WORKERS:-1}"
PORT="${PORT:-5000}"
exec gunicorn --worker-class eventlet -w "$WORKERS" -b 0.0.0.0:"$PORT" app:app