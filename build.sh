#!/usr/bin/env bash
set -o errexit

echo "=== ACTUALIZANDO PIP ==="
pip install --upgrade pip

echo "=== LIMPIANDO CACHE ==="
pip cache purge

echo "=== INSTALANDO DEPENDENCIAS ==="
pip install -r requirements.txt

echo "=== APLICANDO MIGRACIONES ==="
python manage.py migrate

echo "=== COLECTANDO ARCHIVOS ESTÁTICOS ==="
python manage.py collectstatic --noinput --clear

echo "=== BUILD COMPLETADO EXITOSAMENTE ==="
