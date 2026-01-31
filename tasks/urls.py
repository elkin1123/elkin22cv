from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Rutas principales
    path('experiencia/', views.experiencia, name='experiencia'),
    path('cursos/', views.cursos, name='cursos'),
    path('reconocimientos/', views.reconocimientos, name='reconocimientos'),
    path('productos-laborales/', views.productos_laborales, name='productos_laborales'),
    path('productos-academicos/', views.productos_academicos, name='productos_academicos'),
    path('garage/', views.garage, name='garage'),
    
    # Dos opciones para PDF:
    path('exportar-cv/', views.exportar_cv, name='exportar_cv'),  # Solo CV simple
    path('pdf-completo/', views.pdf_datos_personales, name='pdf_completo'),  # Con certificados
    
    # Rutas auxiliares
    path('health/', views.health_check, name='health'),
    path('error/', views.error_page, name='error'),
]