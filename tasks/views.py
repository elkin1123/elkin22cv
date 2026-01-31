from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, ExperienciaLaboral, 
    CursoRealizado, Reconocimiento, 
    ProductoAcademico, ProductoLaboral, VentaGarage
)

# --- Funciones Auxiliares ---

def get_active_profile():
    """Obtiene el perfil marcado como activo."""
    return DatosPersonales.objects.filter(perfilactivo=1).first()

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

# --- Exportar CV en PDF ---

def exportar_cv(request):
    """Vista para exportar el CV en PDF"""
    try:
        perfil = get_active_profile()
        if not perfil:
            return HttpResponse("No hay perfil activo", status=404)
        
        # Obtener datos
        experiencias = ExperienciaLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        cursos_list = CursoRealizado.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        reconocimientos_list = Reconocimiento.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        productos_acad = ProductoAcademico.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        productos_lab = ProductoLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
        
        # Cargar plantilla
        template = get_template('cv.html')
        
        # Renderizar con contexto
        html_content = template.render({
            'perfil': perfil,
            'experiencias': experiencias,
            'cursos': cursos_list,
            'reconocimientos': reconocimientos_list,
            'productos_academicos': productos_acad,
            'productos_laborales': productos_lab,
            'pdf_mode': True,
        })
        
        # Crear PDF
        response = HttpResponse(content_type='application/pdf')
        filename = f"CV_{perfil.nombres}_{perfil.apellidos}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=response,
            encoding='UTF-8'
        )
        
        if pisa_status.err:
            return HttpResponse('Error al generar PDF', status=500)
        
        return response
        
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)