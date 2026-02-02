#!/usr/bin/env bash
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar migraciones (CREA LAS TABLAS)
python manage.py migrate

# 3. Crear superusuario automáticamente
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

# Estas son las credenciales por defecto
username = "admin"
email = "elkinjoshuadelgadolesp68@gmail.com"
password = "Admin123456!"

# Intentar obtener de variables de entorno (Render)
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", username)
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", email)
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", password)

# Crear si no existe
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superusuario '{username}' creado exitosamente")
else:
    print(f"ℹ️ El usuario '{username}' ya existe")
EOF

# 4. Archivos estáticos (AL FINAL)
python manage.py collectstatic --noinput