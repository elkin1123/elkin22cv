#!/usr/bin/env bash
# build.sh - Script para construir la aplicación en Render

echo "=== INICIANDO BUILD ==="

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Aplicar migraciones de base de datos
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Colectar archivos estáticos
echo "Colectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "=== BUILD COMPLETADO ==="