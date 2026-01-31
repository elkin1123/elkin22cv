from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('experiencia/', views.experiencia, name='experiencia'),
    path('cursos/', views.cursos, name='cursos'),
    path('reconocimientos/', views.reconocimientos, name='reconocimientos'),
    path('productos-laborales/', views.productos_laborales, name='productos_laborales'),
    path('productos-academicos/', views.productos_academicos, name='productos_academicos'),
    path('garage/', views.garage, name='garage'),

    path('exportar-cv/', views.exportar_cv, name='exportar_cv'),
]
