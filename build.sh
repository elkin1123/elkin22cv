#!/usr/bin/env bash
# build.sh - PARA NUEVA BASE DE DATOS
set -o errexit

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser --noinput --username admin --email admin@admin.com || true