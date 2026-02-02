"""
Django settings for cv_elkin project.
"""

import os
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv  # <-- AÑADE ESTO

# Cargar variables de entorno del archivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY / DEBUG
# =========================
SECRET_KEY = os.environ.get('SECRET_KEY', 'iy-z-0qT3MHUL4p5Y-0_213HMJL5sBxTe8dL4ergAuvVwVhV0EK0XGFZ68S4FBV_I0s')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# =========================
# ALLOWED HOSTS (Render)
# =========================
ALLOWED_HOSTS = []

# Configuración para Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

# =========================
# APPS (CON CLOUDINARY) - CORREGIDO
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Cloudinary apps
    'cloudinary',
    'cloudinary_storage',
    
    # Tu app - CORREGIDO
    'tasks',  # SOLO 'tasks', NO 'tasks.apps.PerfilConfig'
]

# =========================
# MIDDLEWARE (Con Whitenoise)
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cv_elkin.urls'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cv_elkin.wsgi.application'

# =========================
# DATABASE (PostgreSQL en Render) - CORREGIDO
# =========================

# Esta es la configuración que tus compañeros realmente usan
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',  # Para desarrollo local
        conn_max_age=600
    )
}

# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / 'static',
] if os.path.exists(BASE_DIR / 'static') else []

# =========================
# MEDIA FILES & CLOUDINARY - CORREGIDO
# =========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'dsz84kt2o'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '51793893355762'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

# Configuración STORAGES para Django 4.2+ (sin DEFAULT_FILE_STORAGE)
# Solo usar Cloudinary si tenemos las 3 claves
if (CLOUDINARY_STORAGE['CLOUD_NAME'] and 
    CLOUDINARY_STORAGE['API_KEY'] and 
    CLOUDINARY_STORAGE['API_SECRET']):
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    print("✅ Cloudinary activado para archivos media")
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    print("Cloudinary NO configurado, usando sistema de archivos local")


# =========================
# DEFAULT AUTO FIELD
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# SECURITY HEADERS (RENDER)
# =========================
if RENDER_EXTERNAL_HOSTNAME:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [
        f'https://{RENDER_EXTERNAL_HOSTNAME}',
        'https://*.onrender.com',
    ]
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# =========================
# X-FRAME OPTIONS
# =========================
X_FRAME_OPTIONS = 'SAMEORIGIN'

# =========================
# AUTO CREATE SUPERUSER - MOVIDO A UN LUGAR MÁS SEGURO
# =========================
# Nota: La creación automática de superusuario se ha removido de settings.py
# para evitar errores durante el inicio. En su lugar, crea un management command
# o usa un signal (e.g., en apps.py de tu app) para crearlo después de las migraciones.
# Ejemplo de command: python manage.py createsuperuser --noinput (con variables de entorno)