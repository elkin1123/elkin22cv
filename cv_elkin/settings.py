"""
Django settings for cv_elkin project.
"""

import os
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

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
    ALLOWED_HOSTS.append(f'www.{RENDER_EXTERNAL_HOSTNAME}')
else:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '0.0.0.0'])

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
    
    # Tu app
    'tasks',
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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'cv_elkin.wsgi.application'

# =========================
# DATABASE (PostgreSQL en Render) - CORREGIDO
# =========================

# Esta es la configuración que tus compañeros realmente usan
# En cv_elkin/settings.py, CAMBIA la configuración de DATABASES a:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
# STATIC FILES
# =========================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / 'static',
] if os.path.exists(BASE_DIR / 'static') else []

# Configuración de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# MEDIA FILES & CLOUDINARY - CORREGIDO
# =========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de Cloudinary
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', 'dsz84kt2o')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '51793893355762')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}

# Solo usar Cloudinary si tenemos las 3 claves configuradas
CLOUDINARY_CONFIGURED = all([
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
])

if CLOUDINARY_CONFIGURED:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    print("✅ Cloudinary activado para archivos media")
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    print("⚠️ Cloudinary NO configurado, usando sistema de archivos local para media")

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
        f'https://www.{RENDER_EXTERNAL_HOSTNAME}',
        'https://*.onrender.com',
        'https://*.up.railway.app',
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
# LOGGING (Opcional, para debug)
# =========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

# =========================
# IMPORTANTE PARA PDF Y ESTÁTICOS
# =========================
# Asegurar que whitenoise sirva archivos estáticos correctamente
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True