# 📋 Funcionalidad de Cédula Profesional

## Descripción
Sistema de verificación de identidad para profesores mediante la carga de imagen de cédula profesional.

## 🎯 Características

### Para Profesores
- **Subir cédula profesional**: Los profesores pueden subir una imagen de su cédula profesional
- **Visualización**: La cédula se muestra en el dashboard con opción de ampliar
- **Estado de verificación**: Indica si la cédula está verificada o pendiente
- **Actualización**: Permite actualizar la imagen de la cédula en cualquier momento

### Para Administradores
- **Verificación manual**: Los administradores pueden revisar y verificar las cédulas
- **Control de acceso**: Se puede condicionar funcionalidades según el estado de verificación

## 📁 Archivos Modificados

### Modelos (models.py)
```python
class Teacher(db.Model):
    cedula_profesional_img = db.Column(db.String(300), nullable=True)
    cedula_verified = db.Column(db.Boolean, default=False)
```

### Rutas (app.py)
- `POST /teacher/upload_cedula`: Ruta para subir imagen de cédula

### Templates
- `teacher_dashboard.html`: Sección de cédula profesional agregada al inicio del dashboard

### Estilos
- `teacher_dashboard.css`: Estilos responsivos para la sección de cédula

## 🚀 Instalación

### 1. Ejecutar Migración de Base de Datos

**Opción A - Script Python (Recomendado):**
```bash
python migrate_cedula.py
```

**Opción B - SQL Manual:**
```bash
# Para PostgreSQL
psql -U tu_usuario -d tu_base_datos -f migrations/add_cedula_fields.sql

# Para SQLite (dentro de Python)
python
>>> from app import app, db
>>> from sqlalchemy import text
>>> with app.app_context():
...     with db.engine.connect() as conn:
...         conn.execute(text("ALTER TABLE teachers ADD COLUMN cedula_profesional_img VARCHAR(300)"))
...         conn.execute(text("ALTER TABLE teachers ADD COLUMN cedula_verified BOOLEAN DEFAULT 0"))
...         conn.commit()
```

### 2. Verificar Carpeta de Uploads
La carpeta `static/uploads/cedulas/` se crea automáticamente al subir la primera imagen.

## 📖 Uso

### Para Profesores

1. **Acceder al Dashboard del Profesor**
   - Ir a `/teacher/dashboard`

2. **Subir Cédula Profesional**
   - Si no hay cédula: Hacer clic en "Subir Cédula Profesional"
   - Si ya existe: Hacer clic en "Actualizar Cédula"
   - Seleccionar imagen (PNG, JPG, JPEG, GIF, WEBP)
   - Confirmar la carga

3. **Ver Estado de Verificación**
   - ⏰ **Pendiente**: Cédula subida pero no verificada
   - ✅ **Verificada**: Cédula aprobada por administrador

4. **Ampliar Imagen**
   - Hacer clic en la imagen de la cédula para verla en tamaño completo

## 🔒 Seguridad

### Validaciones Implementadas
- ✅ Solo usuarios autenticados como profesores pueden subir cédulas
- ✅ Validación de tipos de archivo (solo imágenes)
- ✅ Nombres de archivo seguros con `secure_filename()`
- ✅ Nombres únicos con timestamp para evitar sobrescrituras
- ✅ Eliminación automática de imagen anterior al actualizar

### Formatos Aceptados
- PNG
- JPG / JPEG
- GIF
- WEBP

## 📱 Responsive Design

La sección de cédula es completamente responsiva:

- **Desktop**: Vista en dos columnas (info + imagen)
- **Tablet**: Vista adaptada con columnas flexibles
- **Mobile**: Vista apilada verticalmente
- **Imágenes**: Se ajustan automáticamente al contenedor

## 🎨 Estilos

La sección usa el mismo tema visual que el resto del dashboard:

- Paleta de colores: `--primary-color`, `--accent-color`, etc.
- Tipografía: Poppins, Exo 2
- Sombras y bordes consistentes
- Animaciones y transiciones suaves

## 🔄 Flujo de Verificación

```
1. Profesor sube cédula
   ↓
2. Estado: Pendiente (cedula_verified = False)
   ↓
3. Administrador revisa cédula
   ↓
4. Administrador verifica/rechaza
   ↓
5. Estado actualizado en base de datos
   ↓
6. Profesor ve estado actualizado en dashboard
```

## 📊 Estructura de Base de Datos

```sql
teachers
├── id (INTEGER, PRIMARY KEY)
├── user_id (INTEGER, FOREIGN KEY)
├── area (VARCHAR(50))
├── cedula_profesional_img (VARCHAR(300))  -- NUEVO
├── cedula_verified (BOOLEAN)              -- NUEVO
└── created_at (DATETIME)
```

## 🐛 Troubleshooting

### Error: "No se ha seleccionado ningún archivo"
- **Solución**: Asegúrate de seleccionar un archivo antes de hacer clic en "Subir"

### Error: "Formato de archivo no válido"
- **Solución**: Solo se aceptan imágenes (PNG, JPG, JPEG, GIF, WEBP)

### Error: "No tienes perfil de profesor"
- **Solución**: Solo los usuarios con perfil de profesor pueden subir cédulas

### La imagen no se muestra
- **Verificar**: Que la ruta en la base de datos sea correcta
- **Verificar**: Que el archivo exista en `static/uploads/cedulas/`
- **Verificar**: Permisos de lectura en la carpeta

## 🔮 Futuras Mejoras

- [ ] Validación automática con OCR
- [ ] Notificación al profesor cuando se verifica la cédula
- [ ] Historial de cédulas subidas
- [ ] Compresión automática de imágenes grandes
- [ ] Crop y ajuste de imagen antes de subir
- [ ] Verificación con base de datos oficial de cédulas profesionales

## 📝 Notas Adicionales

- Las imágenes se almacenan localmente en el servidor
- Cada profesor puede tener solo una cédula activa
- Las cédulas antiguas se eliminan automáticamente al subir una nueva
- El estado de verificación debe ser actualizado manualmente por un administrador

## 👥 Créditos

Desarrollado para MenTora - Plataforma educativa gamificada
