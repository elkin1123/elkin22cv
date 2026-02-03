import io
import os
import requests
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings

# INTENTAR IMPORTAR xhtml2pdf con manejo de errores
try:
    from xhtml2pdf import pisa
    XHTML2PDF_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ xhtml2pdf no disponible: {e}")
    XHTML2PDF_AVAILABLE = False
    # Crear objeto dummy para evitar errores
    class PisaDummy:
        def CreatePDF(self, *args, **kwargs):
            raise ImportError("xhtml2pdf no está instalado correctamente")
    pisa = PisaDummy()

# INTENTAR IMPORTAR pypdf con manejo de errores
try:
    from pypdf import PdfWriter
    PYPDF_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ pypdf no disponible: {e}")
    PYPDF_AVAILABLE = False
    # Crear objeto dummy
    class PdfWriterDummy:
        def __init__(self):
            pass
        def append(self, *args, **kwargs):
            pass
        def write(self, *args, **kwargs):
            pass
        def close(self):
            pass
    PdfWriter = PdfWriterDummy

# Import desde tasks.models
from .models import (
    DatosPersonales, ExperienciaLaboral, 
    CursoRealizado, Reconocimiento, 
    ProductoAcademico, ProductoLaboral, VentaGarage
)

# --- Funciones Auxiliares ---

def get_active_profile():
    """Obtiene el perfil marcado como activo."""
    return DatosPersonales.objects.filter(perfilactivo=1).first()

def get_image_base64(url, request=None):
    """Convierte imagen de URL a Base64."""
    try:
        # Si es una ruta local
        if url.startswith('/'):
            if request:
                # Construir URL completa
                url = request.build_absolute_uri(url)
            else:
                # En producción
                import os
                render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
                if render_host and not settings.DEBUG:
                    url = f"https://{render_host}{url}"
        
        # Descargar la imagen
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', 'image/jpeg')
            encoded_string = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{encoded_string}"
    
    except Exception as e:
        print(f"Error en get_image_base64: {e}")
        return None
    
    return None

# --- Vistas Principales ---

def home(request):
    perfil = get_active_profile()
    if not perfil:
        return render(request, 'home.html', {'perfil': None})

    context = {
        'perfil': perfil,
        'resumen_exp': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_cursos': CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_rec': Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_acad': ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_lab': ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_garage': VentaGarage.objects.all()[:5],
    }
    return render(request, 'home.html', context)

# --- Vistas de Navegación ---

def experiencia(request):
    perfil = get_active_profile()
    if not perfil:
        return render(request, 'experiencia.html', {'experiencias': [], 'perfil': None})
    
    exp_list = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'experiencia.html', {'experiencias': exp_list, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    if not perfil:
        return render(request, 'productos_academicos.html', {'productos_academicos': [], 'perfil': None})
    
    prod_acad = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'productos_academicos.html', {'productos_academicos': prod_acad, 'perfil': perfil})

def productos_laborales(request):
    perfil = get_active_profile()
    if not perfil:
        return render(request, 'productos_laborales.html', {'productos_laborales': [], 'perfil': None})
    
    prod_lab = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'productos_laborales.html', {'productos_laborales': prod_lab, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    if not perfil:
        return render(request, 'cursos.html', {'cursos': [], 'perfil': None})
    
    cursos_list = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'cursos.html', {'cursos': cursos_list, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    if not perfil:
        return render(request, 'reconocimientos.html', {'reconocimientos': [], 'perfil': None})
    
    reco_list = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'reconocimientos.html', {'reconocimientos': reco_list, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    items = VentaGarage.objects.all()
    return render(request, 'garage.html', {'garage_items': items, 'perfil': perfil})

def exportar_cv(request):
    return pdf_datos_personales(request)

# --- Generación de PDF (CON MANEJO DE ERRORES) ---

def pdf_datos_personales(request):
    # Verificar dependencias primero
    if not XHTML2PDF_AVAILABLE or not PYPDF_AVAILABLE:
        return HttpResponse("""
            <html>
            <body style="font-family: Arial; padding: 20px;">
                <h1>❌ Error: Dependencias faltantes</h1>
                <p>Las bibliotecas necesarias para generar PDF no están instaladas correctamente.</p>
                <p>Contacta al administrador del sistema.</p>
                <p><a href="/">← Volver al inicio</a></p>
            </body>
            </html>
        """, status=500)
    
    # Obtener perfil activo
    try:
        perfil = DatosPersonales.objects.get(perfilactivo=1)
    except DatosPersonales.DoesNotExist:
        return HttpResponse("""
            <html>
            <body style="font-family: Arial; padding: 20px;">
                <h1>❌ Error: No hay perfil activo</h1>
                <p>Para generar el PDF, crea un perfil en el admin y márcalo como activo (perfilactivo=1).</p>
                <p><a href="/admin/">Ir al admin</a> | <a href="/">← Volver al inicio</a></p>
            </body>
            </html>
        """, status=404)
    
    # Obtener datos
    foto_base64 = None
    if perfil.foto:
        foto_url = perfil.foto.url
        if not (foto_url.startswith('http://') or foto_url.startswith('https://')):
            foto_url = request.build_absolute_uri(perfil.foto.url)
        foto_base64 = get_image_base64(foto_url, request)
    
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    academicos = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    laborales = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    cursos_objs = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    reco_objs = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    
    # Renderizar template
    template = get_template('cv_pdf_maestro.html')
    html = template.render({
        'perfil': perfil, 
        'foto_pdf': foto_base64,
        'items': experiencias, 
        'productos': academicos,
        'productos_laborales': laborales, 
        'cursos': cursos_objs, 
        'reconocimientos': reco_objs
    })
    
    # Crear PDF
    try:
        buffer_cv = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=buffer_cv)
        
        if pisa_status.err:
            raise Exception(f"Error generando PDF: {pisa_status.err}")
        
        # Crear PDF final
        writer = PdfWriter()
        buffer_cv.seek(0)
        writer.append(buffer_cv)
        
        # Añadir certificados si existen
        def añadir_certificados(queryset):
            for obj in queryset:
                if obj.rutacertificado:
                    try:
                        cert_url = obj.rutacertificado.url
                        if not (cert_url.startswith('http://') or cert_url.startswith('https://')):
                            cert_url = request.build_absolute_uri(obj.rutacertificado.url)
                        
                        response = requests.get(cert_url, timeout=10)
                        if response.status_code == 200:
                            writer.append(io.BytesIO(response.content))
                    except Exception as e:
                        print(f"Error añadiendo certificado: {e}")
                        continue
        
        añadir_certificados(cursos_objs)
        añadir_certificados(reco_objs)
        
        # Devolver respuesta
        response = HttpResponse(content_type='application/pdf')
        nombre_archivo = f"CV_{perfil.apellidos}_{perfil.nombres}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        
        writer.write(response)
        writer.close()
        
        return response
        
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        return HttpResponse(f"""
            <html>
            <body style="font-family: Arial; padding: 20px;">
                <h1>❌ Error generando PDF</h1>
                <p>Error: {str(e)}</p>
                <p><a href="/">← Volver al inicio</a></p>
            </body>
            </html>
        """, status=500)