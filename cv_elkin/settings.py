"""
Django settings for cv_elkin project.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY / DEBUG
# =========================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-cambiar-en-produccion')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# =========================
# ALLOWED HOSTS (Render)
# =========================
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Configuración para Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# =========================
# APPS (CON CLOUDINARY)
# =========================
I# En INSTALLED_APPS, asegúrate que estén en ESTE ORDEN:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Cloudinary apps (IMPORTANTE: antes de staticfiles)
    'cloudinary_storage',  # PRIMERO
    'cloudinary',          # SEGUNDO
    'django.contrib.staticfiles',  # TERCERO
    
    # Tu app
    'tasks',
]

# =========================
# MIDDLEWARE (Con Whitenoise)
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para archivos estáticos
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
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta global de templates
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
# DATABASE (PostgreSQL en Render)
# =========================
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # SQLite solo para desarrollo local
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
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
# STATIC FILES (Whitenoise)
# =========================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Solo si tienes esta carpeta

# WhiteNoise para archivos estáticos comprimidos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# MEDIA FILES (Cloudinary - IMPORTANTE)
# =========================
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}

# Usa Cloudinary para almacenar imágenes
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Configuración local de media (solo referencia)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# SECURITY HEADERS (Render)
# =========================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]

# Activar estas opciones solo en producción
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# =========================
# DEFAULT AUTO FIELD
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'