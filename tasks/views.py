import io
import os
import requests
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from pypdf import PdfWriter 

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
    """Convierte imagen de URL a Base64 para que xhtml2pdf la renderice."""
    try:
        # Si es una ruta local (empieza con /media/ o /)
        if url.startswith('/'):
            # Manejar archivos en MEDIA_ROOT
            if url.startswith(settings.MEDIA_URL):
                # Quita /media/ del inicio
                media_path = url.replace(settings.MEDIA_URL, '', 1)
                # Construye la ruta completa
                file_path = os.path.join(settings.MEDIA_ROOT, media_path)
            else:
                # Ruta absoluta en el sistema de archivos
                file_path = url
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                    # Determina el tipo de imagen
                    file_ext = file_path.split('.')[-1].lower()
                    if file_ext == 'jpg' or file_ext == 'jpeg':
                        content_type = 'image/jpeg'
                    elif file_ext == 'png':
                        content_type = 'image/png'
                    elif file_ext == 'gif':
                        content_type = 'image/gif'
                    else:
                        content_type = 'image/jpeg'
                    
                    encoded_string = base64.b64encode(content).decode('utf-8')
                    return f"data:{content_type};base64,{encoded_string}"
        
        # Si es una URL completa (http:// o https://)
        elif url.startswith('http://') or url.startswith('https://'):
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', 'image/jpeg')
                encoded_string = base64.b64encode(response.content).decode('utf-8')
                return f"data:{content_type};base64,{encoded_string}"
    
    except Exception as e:
        print(f"Error en get_image_base64 para URL {url}: {e}")
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

# --- Generación de PDF (MEJORADA) ---

def pdf_datos_personales(request):
    # Primero intenta obtener el perfil activo
    try:
        perfil = DatosPersonales.objects.get(perfilactivo=1)
    except DatosPersonales.DoesNotExist:
        # Si no existe, muestra error
        return HttpResponse("""
            <html>
            <head><title>Error - No hay perfil activo</title></head>
            <body style="font-family: Arial; padding: 40px;">
                <h1>❌ Error: No hay perfil activo</h1>
                <p>Para generar el PDF, primero debes crear un perfil y marcarlo como activo.</p>
                <h3>Pasos a seguir:</h3>
                <ol>
                    <li>Ve al <a href="/admin/tasks/datospersonales/">Panel de Administración</a></li>
                    <li>Crea un nuevo perfil en "Datos Personales"</li>
                    <li><strong>IMPORTANTE:</strong> Establece "perfilactivo" en <strong>1</strong></li>
                    <li>Guarda el perfil</li>
                    <li>Vuelve a intentar generar el PDF</li>
                </ol>
                <p><a href="/">← Volver al inicio</a></p>
            </body>
            </html>
        """, status=404)
    
    # Obtiene la imagen en base64
    foto_base64 = None
    if perfil.foto:
        # Construye la URL completa para el archivo
        foto_url = perfil.foto.url
        if not (foto_url.startswith('http://') or foto_url.startswith('https://')):
            # Es una ruta local, agregamos el dominio para la petición interna
            foto_url = request.build_absolute_uri(perfil.foto.url)
        foto_base64 = get_image_base64(foto_url)
    
    # Obtiene todos los datos relacionados
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    academicos = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    laborales = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    cursos_objs = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    reco_objs = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    garage_objs = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    
    # Obtiene imágenes de garage
    imagenes_garage = []
    for item in garage_objs:
        if item.foto:
            foto_url = item.foto.url
            if not (foto_url.startswith('http://') or foto_url.startswith('https://')):
                foto_url = request.build_absolute_uri(item.foto.url)
            img_base64 = get_image_base64(foto_url)
            if img_base64:
                imagenes_garage.append({
                    'nombre': item.nombreproducto,
                    'imagen': img_base64,
                    'descripcion': item.descripcion,
                    'precio': item.valordelbien
                })
    
    # Renderiza el template HTML
    template = get_template('cv_pdf_maestro.html')
    html = template.render({
        'perfil': perfil, 
        'foto_pdf': foto_base64,
        'items': experiencias, 
        'productos': academicos,
        'productos_laborales': laborales, 
        'cursos': cursos_objs, 
        'reconocimientos': reco_objs,
        'imagenes_garage': imagenes_garage,
        'garage_items': garage_objs
    })
    
    # Crea el PDF principal
    buffer_cv = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=buffer_cv)
    
    if pisa_status.err:
        return HttpResponse('Error generando el PDF principal')
    
    # Crea el escritor PDF y añade el contenido principal
    writer = PdfWriter()
    buffer_cv.seek(0)
    writer.append(buffer_cv)
    
    # Función para añadir certificados
    def añadir_certificados(queryset, nombre_tipo):
        for obj in queryset:
            if obj.rutacertificado:
                try:
                    cert_url = obj.rutacertificado.url
                    if not (cert_url.startswith('http://') or cert_url.startswith('https://')):
                        cert_url = request.build_absolute_uri(obj.rutacertificado.url)
                    
                    response = requests.get(cert_url, timeout=10)
                    if response.status_code == 200:
                        writer.append(io.BytesIO(response.content))
                        print(f"✅ Certificado de {nombre_tipo} añadido: {obj}")
                except Exception as e: 
                    print(f"❌ Error añadiendo certificado de {nombre_tipo}: {e}")
                    continue
    
    # Añade certificados de cursos, reconocimientos y experiencia
    añadir_certificados(cursos_objs, "curso")
    añadir_certificados(reco_objs, "reconocimiento")
    añadir_certificados(experiencias, "experiencia laboral")
    
    # Crea la respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    nombre_archivo = f"Portafolio_{perfil.apellidos}_{perfil.nombres}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    
    # Escribe el PDF en la respuesta
    writer.write(response)
    writer.close()
    
    return response