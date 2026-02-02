from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('experiencia/', views.experiencia, name='experiencia'),
    path('cursos/', views.cursos, name='cursos'),
    path('reconocimientos/', views.reconocimientos, name='reconocimientos'),

    # PDF
    path('exportar-cv/', views.pdf_datos_personales, name='exportar_cv'),
]
