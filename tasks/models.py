# tasks/models.py - VERSIÓN BÁSICA Y FUNCIONAL
from django.db import models

# ========== MODELO DATOS PERSONALES ==========
class DatosPersonales(models.Model):
    descripcionperfil = models.TextField(verbose_name="Descripción del perfil", blank=True, null=True)
    perfilactivo = models.IntegerField(verbose_name="Perfil activo", default=0)
    apellidos = models.CharField(max_length=200, verbose_name="Apellidos")
    nombres = models.CharField(max_length=200, verbose_name="Nombres")
    nacionalidad = models.CharField(max_length=100, verbose_name="Nacionalidad", blank=True, null=True)
    lugarnacimiento = models.CharField(max_length=200, verbose_name="Lugar de nacimiento", blank=True, null=True)
    fechanacimiento = models.DateField(verbose_name="Fecha de nacimiento", blank=True, null=True)
    numerocedula = models.CharField(max_length=20, verbose_name="Número de cédula", blank=True, null=True)
    sexo = models.CharField(max_length=20, verbose_name="Sexo", blank=True, null=True)
    estadocivil = models.CharField(max_length=50, verbose_name="Estado civil", blank=True, null=True)
    licenciaconducir = models.CharField(max_length=50, verbose_name="Licencia de conducir", blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=20, verbose_name="Teléfono convencional", blank=True, null=True)
    telefonofijo = models.CharField(max_length=20, verbose_name="Teléfono fijo", blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=500, verbose_name="Dirección de trabajo", blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=500, verbose_name="Dirección domiciliaria", blank=True, null=True)
    sitioweb = models.URLField(verbose_name="Sitio web", blank=True, null=True)
    foto = models.ImageField(upload_to='fotos/', verbose_name="Foto", blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# ========== MODELO EXPERIENCIA LABORAL ==========
class ExperienciaLaboral(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, verbose_name="Perfil asociado")
    cargodesempenado = models.CharField(max_length=200, verbose_name="Cargo desempeñado")
    nombrempresa = models.CharField(max_length=200, verbose_name="Nombre empresa")
    fechainiciogestion = models.DateField(verbose_name="Fecha inicio gestión")
    fechafingestion = models.DateField(verbose_name="Fecha fin gestión")
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(verbose_name="Activar para front", default=True)
    
    def __str__(self):
        return f"{self.cargodesempenado} - {self.nombrempresa}"

# ========== MODELO PRODUCTOS ACADÉMICOS ==========
class ProductoAcademico(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, verbose_name="Perfil asociado")
    nombrerecurso = models.CharField(max_length=200, verbose_name="Nombre recurso")
    clasificador = models.CharField(max_length=100, verbose_name="Clasificador", blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(verbose_name="Activar para front", default=True)
    
    def __str__(self):
        return self.nombrerecurso

# ========== MODELO PRODUCTOS LABORALES ==========
class ProductoLaboral(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, verbose_name="Perfil asociado")
    nombreproducto = models.CharField(max_length=200, verbose_name="Nombre producto")
    fechaproducto = models.DateField(verbose_name="Fecha producto", blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(verbose_name="Activar para front", default=True)
    
    def __str__(self):
        return self.nombreproducto

# ========== MODELO CURSOS REALIZADOS ==========
class CursoRealizado(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, verbose_name="Perfil asociado")
    nombrecurso = models.CharField(max_length=200, verbose_name="Nombre curso")
    entidadpatrocinadora = models.CharField(max_length=200, verbose_name="Entidad patrocinadora")
    fechafin = models.DateField(verbose_name="Fecha fin")
    totalhoras = models.IntegerField(verbose_name="Total horas", default=0)
    activarparaqueseveaenfront = models.BooleanField(verbose_name="Activar para front", default=True)
    
    def __str__(self):
        return self.nombrecurso

# ========== MODELO RECONOCIMIENTOS ==========
class Reconocimiento(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, verbose_name="Perfil asociado")
    descripcionreconocimiento = models.CharField(max_length=200, verbose_name="Descripción reconocimiento")
    tiporeconocimiento = models.CharField(max_length=100, verbose_name="Tipo reconocimiento", blank=True, null=True)
    fechareconocimiento = models.DateField(verbose_name="Fecha reconocimiento")
    descripcion = models.TextField(verbose_name="Descripción adicional", blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(verbose_name="Activar para front", default=True)
    
    def __str__(self):
        return self.descripcionreconocimiento

# ========== MODELO VENTA GARAGE ==========
class VentaGarage(models.Model):
    nombreproducto = models.CharField(max_length=200, verbose_name="Nombre producto")
    estadoproducto = models.CharField(max_length=50, verbose_name="Estado producto", default="Disponible")
    valordelbien = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor del bien", default=0)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(verbose_name="Activar para front", default=True)
    
    def __str__(self):
        return self.nombreproducto