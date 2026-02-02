from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Crear superusuario automáticamente"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write("❌ Variables de entorno no definidas")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("ℹ️ El superusuario ya existe")
        else:
            User.objects.create_superuser(username, email, password)
            self.stdout.write("✅ Superusuario creado correctamente")
