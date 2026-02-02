from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('experiencia/', views.experiencia, name='experiencia'),
    path('cursos/', views.cursos, name='cursos'),
    path('reconocimientos/', views.reconocimientos, name='reconocimientos'),

    # ✅ AGREGA ESTAS 3 RUTAS FALTANTES:
    path('productos-laborales/', views.productos_laborales, name='productos_laborales'),
    path('productos-academicos/', views.productos_academicos, name='productos_academicos'),
    path('garage/', views.garage, name='garage'),

    # PDF
    path('exportar-cv/', views.pdf_datos_personales, name='exportar_cv'),
]