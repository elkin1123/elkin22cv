from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    
    def ready(self):
        # Importar aquí para evitar importaciones circulares
        try:
            from django.contrib.auth.models import User
            from django.db import OperationalError, ProgrammingError
            
            # Verificar si la tabla de usuarios existe
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@admin.com",
                    password="admin123"
                )
                print("Superusuario 'admin' creado exitosamente")
            else:
                print("El superusuario 'admin' ya existe")
        except (OperationalError, ProgrammingError):
            # Las tablas no existen todavía (migraciones no aplicadas)
            print("Las tablas no están listas. Aplica las migraciones primero.")
            pass