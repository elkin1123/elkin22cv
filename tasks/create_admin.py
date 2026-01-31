from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Crea un superusuario automáticamente si no existe"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@email.com",
                password="admin123"
            )
            self.stdout.write(self.style.SUCCESS("✅ Superusuario creado"))
        else:
            self.stdout.write("📌 Superusuario ya existe")
