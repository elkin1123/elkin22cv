#!/usr/bin/env bash
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar migraciones
python manage.py migrate

# 3. Archivos estáticos
python manage.py collectstatic --noinput
