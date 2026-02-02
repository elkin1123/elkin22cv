from django.contrib import admin
from .models import *

# --- 1. Datos Personales ---
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'descripcionperfil', 'perfilactivo')
    search_fields = ('nombres', 'apellidos', 'numerocedula')
    list_filter = ('perfilactivo', 'nacionalidad', 'sexo')

# --- 2. Experiencia Laboral ---
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainicogestion', 'fechafingestion', 'activarparaqueeseveaenfront')
    list_filter = ('activarparaqueeseveaenfront', 'nombrempresa')
    date_hierarchy = 'fechainicogestion'
    search_fields = ('cargodesempenado', 'nombrempresa')

# --- 3. Productos Académicos ---
@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueeseveaenfront')
    list_filter = ('activarparaqueeseveaenfront', 'clasificador')
    search_fields = ('nombrerecurso', 'descripcion')

# --- 4. Productos Laborales ---
@admin.register(ProductoLaboral)
class ProductoLaboralAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueeseveaenfront')
    list_filter = ('activarparaqueeseveaenfront',)
    search_fields = ('nombreproducto', 'descripcion')

# --- 5. Reconocimientos ---
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'fechareconocimiento', 'activarparaqueeseveaenfront')
    list_filter = ('activarparaqueeseveaenfront', 'tiporeconocimiento')
    date_hierarchy = 'fechareconocimiento'

# --- 6. Cursos Realizados ---
@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'fechafin', 'totalhoras', 'activarparaqueeseveaenfront')
    list_filter = ('activarparaqueeseveaenfront', 'entidadpatrocinadora')
    date_hierarchy = 'fechafin'
    search_fields = ('nombrecurso', 'entidadpatrocinadora')

# --- 7. Venta Garage ---
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombrepreducto', 'estadoproducto', 'valordelbien', 'activparaqueuseveaefront')
    list_filter = ('activparaqueuseveaefront', 'estadoproducto')
    search_fields = ('nombrepreducto',)