from django.apps import AppConfig

class PerfilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin',
                'admin@admin.com',
                'admin123'
            )


"""""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    
    def ready(self):
        # COMENTA O ELIMINA ESTE CÓDIGO TEMPORALMENTE
        # from django.contrib.auth.models import User
        
        # try:
        #     if not User.objects.filter(username='admin').exists():
        #         User.objects.create_superuser(
        #             username='admin',
        #             email='admin@example.com',
        #             password='admin123'
        #         )
        #         print("Superusuario 'admin' creado automáticamente")
        # except Exception as e:
        #     print(f"Error creando superusuario: {e}")
        pass  # Deja solo esta línea
   
""""