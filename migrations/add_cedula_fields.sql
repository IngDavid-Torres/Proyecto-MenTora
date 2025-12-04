-- Migración para agregar campos de cédula profesional a la tabla teachers
-- Fecha: 2025-12-04
-- Descripción: Agrega campos para almacenar la imagen de cédula profesional y su estado de verificación

-- Agregar columna para almacenar la ruta de la imagen de la cédula profesional
ALTER TABLE teachers ADD COLUMN IF NOT EXISTS cedula_profesional_img VARCHAR(300);

-- Agregar columna para el estado de verificación de la cédula
ALTER TABLE teachers ADD COLUMN IF NOT EXISTS cedula_verified BOOLEAN DEFAULT FALSE;

-- Comentarios para documentación
COMMENT ON COLUMN teachers.cedula_profesional_img IS 'Ruta de la imagen de la cédula profesional del profesor';
COMMENT ON COLUMN teachers.cedula_verified IS 'Estado de verificación de la cédula profesional (true = verificada, false = pendiente)';
