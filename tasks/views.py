# views.py - CORREGIDO
import base64
import io
import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from PyPDF2 import PdfWriter  # ¡CORREGIDO! De 'pypdf' a 'PyPDF2'
from .models import (
    DatosPersonales, ExperienciaLaboral, 
    CursoRealizado, Reconocimiento, 
    ProductoAcademico, ProductoLaboral, VentaGarage
)

# --- Funciones Auxiliares ---

def get_active_profile():
    """Obtiene el perfil marcado como activo."""
    return DatosPersonales.objects.filter(perfilactivo=1).first()

def get_image_base64(url):
    """Convierte imagen de URL a Base64 para que xhtml2pdf la renderice."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            encoded_string = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{encoded_string}"
    except Exception:
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
    exp_list = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'experiencia.html', {'experiencias': exp_list, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    prod_acad = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'productos_academicos.html', {'productos_academicos': prod_acad, 'perfil': perfil})

def productos_laborales(request):
    perfil = get_active_profile()
    prod_lab = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'productos_laborales.html', {'productos_laborales': prod_lab, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    cursos_list = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'cursos.html', {'cursos': cursos_list, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    reco_list = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'reconocimientos.html', {'reconocimientos': reco_list, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    items = VentaGarage.objects.all()
    return render(request, 'garage.html', {'garage_items': items, 'perfil': perfil})

# --- VERSIÓN SIMPLE para generar PDF (sin certificados) ---

def exportar_cv(request):
    """Vista simple para exportar solo el CV en PDF"""
    try:
        perfil = get_active_profile()
        if not perfil:
            return render(request, 'cv_error.html', {'message': 'No hay perfil activo'})
        
        # Obtener datos como LISTAS
        experiencias = list(ExperienciaLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ))
        
        cursos_list = list(CursoRealizado.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ))
        
        reconocimientos_list = list(Reconocimiento.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ))
        
        productos_acad = list(ProductoAcademico.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ))
        
        productos_lab = list(ProductoLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ))
        
        # Contexto
        context = {
            'perfil': perfil,
            'experiencias': experiencias,
            'cursos': cursos_list,
            'reconocimientos': reconocimientos_list,
            'productos_academicos': productos_acad,
            'productos_laborales': productos_lab,
            'pdf_mode': True,
        }
        
        # Usar template para PDF
        template = get_template('cv_pdf.html')
        html_content = template.render(context)
        
        # Crear PDF
        response = HttpResponse(content_type='application/pdf')
        filename = f"CV_{perfil.nombres}_{perfil.apellidos}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Convertir HTML a PDF (SIN opciones complejas)
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=response,
            encoding='UTF-8'
        )
        
        if pisa_status.err:
            print(f"ERROR PDF: {pisa_status.err}")
            return HttpResponse(f'Error al generar PDF: {pisa_status.err}', status=500)
        
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR en exportar_cv: {str(e)}")
        
        error_html = f"""
        <html>
        <body style="font-family: Arial; padding: 50px;">
            <h1>Error al generar PDF</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p><strong>Solución:</strong></p>
            <ol>
                <li>Asegúrate de tener un perfil activo en el admin</li>
                <li>Verifica que los modelos tengan datos</li>
                <li>Recarga la página e intenta nuevamente</li>
            </ol>
            <a href="/">Volver al inicio</a>
        </body>
        </html>
        """
        return HttpResponse(error_html, status=500)

# --- VERSIÓN COMPLETA con certificados ---

def pdf_datos_personales(request):
    """Vista para generar PDF completo con certificados (opcional)"""
    try:
        perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
        
        foto_base64 = None
        if perfil.foto:
            # Intentar obtener imagen en base64
            try:
                if perfil.foto.url.startswith('http'):
                    foto_base64 = get_image_base64(perfil.foto.url)
                else:
                    # Para archivos locales
                    with open(perfil.foto.path, 'rb') as f:
                        encoded = base64.b64encode(f.read()).decode('utf-8')
                        foto_base64 = f"data:image/jpeg;base64,{encoded}"
            except Exception as e:
                print(f"Error al procesar foto: {e}")
                foto_base64 = None

        # Obtener datos
        experiencias = ExperienciaLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        
        academicos = ProductoAcademico.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        
        laborales = ProductoLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        
        cursos_objs = CursoRealizado.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        
        reco_objs = Reconocimiento.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )

        # Renderizar template del CV
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
        
        # Crear PDF del CV
        buffer_cv = io.BytesIO()
        pisa_status = pisa.CreatePDF(
            io.BytesIO(html.encode("UTF-8")), 
            dest=buffer_cv
        )
        
        if pisa_status.err:
            return HttpResponse(f'Error al crear PDF: {pisa_status.err}', status=500)
        
        # Crear PDF combinado con certificados
        writer = PdfWriter()
        buffer_cv.seek(0)
        writer.append(buffer_cv)

        # Función para añadir certificados
        def pegar_certificados(queryset):
            for obj in queryset:
                if obj.rutacertificado:
                    try:
                        # Para archivos locales
                        if hasattr(obj.rutacertificado, 'path'):
                            with open(obj.rutacertificado.path, 'rb') as f:
                                writer.append(io.BytesIO(f.read()))
                        # Para URLs
                        elif obj.rutacertificado.url.startswith('http'):
                            r = requests.get(obj.rutacertificado.url, timeout=10)
                            if r.status_code == 200:
                                writer.append(io.BytesIO(r.content))
                    except Exception as e:
                        print(f"Error al agregar certificado {obj}: {e}")
                        continue

        # Añadir certificados de cursos y reconocimientos
        pegar_certificados(cursos_objs)
        pegar_certificados(reco_objs)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Portafolio_{perfil.apellidos}.pdf"'
        writer.write(response)
        writer.close()
        return response
        
    except Exception as e:
        print(f"ERROR en pdf_datos_personales: {str(e)}")
        return HttpResponse(f'Error interno: {str(e)}', status=500)

# --- Vistas auxiliares ---

def health_check(request):
    """Vista simple para verificar que la app funciona"""
    return HttpResponse("✅ ¡La aplicación funciona correctamente!")

def error_page(request):
    """Vista de error genérico"""
    return render(request, 'error.html', {'error': 'Error desconocido'})