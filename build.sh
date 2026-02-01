#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate


# En buildCommand de Render
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    admin_password = os.environ.get('ADMIN_PASSWORD', 'password_temporal')
    User.objects.create_superuser('admin', 'admin@example.com', admin_password)
"