# Guía: Agregar PostgreSQL a MenTora en Railway

## Paso 1: Agregar PostgreSQL al Proyecto

1. **En el dashboard de Railway** (donde ves "Proyecto-MenTora"):
   - Haz clic en el botón **"+ New"** o **"Add Service"**
   - Selecciona **"Database"**
   - Elige **"Add PostgreSQL"**

2. Railway creará automáticamente una instancia de PostgreSQL y generará las credenciales.

## Paso 2: Conectar PostgreSQL al Servicio

Railway automáticamente expone la variable `DATABASE_URL` a todos los servicios del proyecto. Tu código en `config.py` ya está preparado para leerla.

## Paso 3: Variables de Entorno Requeridas

En la pestaña **"Variables"** de tu servicio "Proyecto-MenTora", asegúrate de tener:

### Variables Obligatorias:
```
DATABASE_URL=<se genera automáticamente cuando añades PostgreSQL>
SECRET_KEY=<genera una clave secreta>
PORT=5000
```

### Generar SECRET_KEY:
Ejecuta localmente o en cualquier terminal Python:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```
Copia el resultado y úsalo como valor de `SECRET_KEY`.

### Variables Opcionales:
```
SEED_ON_DEPLOY=1          # Si quieres ejecutar seeds.py en cada deploy
WORKERS=1                 # Número de workers de Gunicorn (1 es óptimo para SocketIO)
FLASK_ENV=production
```

## Paso 4: Configuración del Comando de Start

Railway debería detectar automáticamente el `Procfile`, pero si no:

1. Ve a **Settings** del servicio
2. En **"Deploy"** → **"Start Command"**
3. Asegúrate que sea:
   ```
   gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:$PORT app:app
   ```

## Paso 5: Ejecutar Seeds (Primera Vez)

### Opción A - Manual (Recomendado primera vez):
1. En Railway, ve a tu servicio PostgreSQL
2. Copia la `DATABASE_URL`
3. Localmente, crea archivo `.env`:
   ```
   DATABASE_URL=<pega la URL aquí>
   SECRET_KEY=<tu clave secreta>
   ```
4. Ejecuta:
   ```powershell
   python seeds.py
   ```

### Opción B - Automático en Deploy:
1. Añade variable `SEED_ON_DEPLOY=1`
2. El script `railway.sh` lo ejecutará automáticamente

## Paso 6: Re-Deploy

Después de agregar PostgreSQL:
1. Haz un commit vacío si es necesario: `git commit --allow-empty -m "trigger redeploy"`
2. Push: `git push`
3. Railway hará el deploy automático

## Verificación

1. Ve a **"Deployments"** y espera "Deployment successful"
2. Haz clic en **"View logs"**
3. Deberías ver:
   ```
   ✅ Dependencias listas
   🗄️ Asegurando tablas de base de datos
   Tablas OK
   🔥 Lanzando servidor Gunicorn + Eventlet
   ```

## Estructura Final del Proyecto

```
tender-luck (Proyecto Railway)
├── Proyecto-MenTora (Servicio Web)
│   ├── Variables:
│   │   ├── DATABASE_URL (referencia automática a PostgreSQL)
│   │   ├── SECRET_KEY
│   │   └── PORT
│   └── Connected to: PostgreSQL
└── PostgreSQL (Database)
    └── Proporciona: DATABASE_URL
```

## Troubleshooting

### Error: "relation does not exist"
- Las tablas no se crearon. Verifica logs de Railway o ejecuta seeds.py manualmente.

### Error: "could not connect to server"
- Verifica que PostgreSQL esté en el mismo proyecto Railway.
- Railway conecta servicios del mismo proyecto automáticamente.

### Error: "No module named 'psycopg2'"
- Añade a `requirements.txt`: `psycopg2-binary==2.9.9`

### App no responde:
- Verifica que el `Procfile` use `gunicorn` (no `python app.py`)
- Revisa logs en Railway para ver errores específicos

## Conexión Local a PostgreSQL de Railway

Si quieres desarrollo local contra la DB de Railway:

1. Copia `DATABASE_URL` desde Railway
2. Crea `.env` local:
   ```
   DATABASE_URL=postgresql://postgres:...
   SECRET_KEY=tu_clave_local
   ```
3. Ejecuta: `python app.py`

¡Listo! Tu app MenTora ahora usa PostgreSQL en Railway.
