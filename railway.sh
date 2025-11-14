#!/bin/bash
# Railway build script

echo "🚀 Iniciando build de MenTora..."

# Instalar dependencias de Python
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completado"