#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip primero
pip install --upgrade pip

# Instalar las versiones ESPECÍFICAS para evitar conflictos
echo "Instalando Django..."
pip install Django==4.2.10

echo "Instalando reportlab compatible..."
pip install reportlab==3.6.12

echo "Instalando xhtml2pdf compatible..."
pip install xhtml2pdf==0.2.5

echo "Instalando otras dependencias críticas..."
pip install pypdf==3.17.1
pip install Pillow==10.1.0
pip install requests==2.31.0
pip install whitenoise==6.6.0
pip install psycopg2-binary==2.9.9
pip install dj-database-url==2.1.0
pip install python-dotenv==1.0.0
pip install cloudinary==1.36.0
pip install django-cloudinary-storage==0.3.0

# Ahora instalar el resto si hay requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Instalando dependencias adicionales de requirements.txt..."
    pip install -r requirements.txt
fi

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py makemigrations --noinput || echo "No hay migraciones nuevas"
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --no-input --clear

# Crear superusuario automáticamente
echo "Verificando superusuario..."
python << END
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv_elkin.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
password = os.environ.get('ADMIN_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Superusuario {username} creado automáticamente')
else:
    print(f'✅ Superusuario {username} ya existe')
END

echo "✅ Build completado exitosamente!"