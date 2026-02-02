import io
import requests
import base64

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from pypdf import PdfWriter

# ✅ IMPORT CORRECTO
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    CursoRealizado,
    Reconocimiento,
    ProductoAcademico,
    ProductoLaboral,
    VentaGarage
)

# -------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------

def get_active_profile():
    """Obtiene el perfil activo (perfilactivo=1)."""
    return DatosPersonales.objects.filter(perfilactivo=1).first()

def get_image_base64(url):
    """Convierte imagen en Base64 para xhtml2pdf."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get("content-type")
            encoded = base64.b64encode(response.content).decode("utf-8")
            return f"data:{content_type};base64,{encoded}"
    except Exception:
        return None
    return None

# -------------------------------------------------
# VISTAS NORMALES
# -------------------------------------------------

def home(request):
    perfil = get_active_profile()
    return render(request, "home.html", {"perfil": perfil})

def experiencia(request):
    perfil = get_active_profile()
    experiencias = ExperienciaLaboral.objects.filter(
        idperfilconqueestaativo=perfil,
        activarparaqueeseveaenfront=True
    )
    return render(request, "experiencia.html", {"perfil": perfil, "experiencias": experiencias})

def cursos(request):
    perfil = get_active_profile()
    cursos = CursoRealizado.objects.filter(
        idperfilconqueestaativo=perfil,
        activarparaqueeseveaenfront=True
    )
    return render(request, "cursos.html", {"perfil": perfil, "cursos": cursos})

def reconocimientos(request):
    perfil = get_active_profile()
    reconocimientos = Reconocimiento.objects.filter(
        idperfilconqueestaativo=perfil,
        activarparaqueeseveaenfront=True
    )
    return render(request, "reconocimientos.html", {"perfil": perfil, "reconocimientos": reconocimientos})

# -------------------------------------------------
# VISTAS NUEVAS (AGREGA ESTAS)
# -------------------------------------------------

def productos_laborales(request):
    perfil = get_active_profile()
    productos = ProductoLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueeseveaenfront=True
    )
    return render(request, "productos_laborales.html", {
        "perfil": perfil,
        "productos_laborales": productos
    })

def productos_academicos(request):
    perfil = get_active_profile()
    productos = ProductoAcademico.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueeseveaenfront=True
    )
    return render(request, "productos_academicos.html", {
        "perfil": perfil,
        "productos_academicos": productos
    })

def garage(request):
    perfil = get_active_profile()
    items = VentaGarage.objects.filter(
        idperfilconqueestaatcivo=perfil,
        activparaqueuseveaefront=True
    )
    return render(request, "garage.html", {
        "perfil": perfil,
        "garage_items": items
    })

# -------------------------------------------------
# PDF PRINCIPAL
# -------------------------------------------------

def pdf_datos_personales(request):
    # ✅ EVITA MultipleObjectsReturned
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if not perfil:
        return HttpResponse("No existe un perfil activo", status=404)

    foto_base64 = None
    if perfil.foto:
        foto_base64 = get_image_base64(perfil.foto.url)

    experiencias = ExperienciaLaboral.objects.filter(
        idperfilconqueestaativo=perfil,
        activarparaqueeseveaenfront=True
    )

    productos_acad = ProductoAcademico.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueeseveaenfront=True
    )

    productos_lab = ProductoLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueeseveaenfront=True
    )

    cursos = CursoRealizado.objects.filter(
        idperfilconqueestaativo=perfil,
        activarparaqueeseveaenfront=True
    )

    reconocimientos = Reconocimiento.objects.filter(
        idperfilconqueestaativo=perfil,
        activarparaqueeseveaenfront=True
    )

    template = get_template("cv_pdf.html")
    html = template.render({
        "perfil": perfil,
        "foto_pdf": foto_base64,
        "items": experiencias,
        "productos": productos_acad,
        "productos_laborales": productos_lab,
        "cursos": cursos,
        "reconocimientos": reconocimientos
    })

    buffer_principal = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=buffer_principal)

    writer = PdfWriter()
    buffer_principal.seek(0)
    writer.append(buffer_principal)

    def anexar_certificados(queryset):
        for obj in queryset:
            if obj.rutacertificado:
                try:
                    r = requests.get(obj.rutacertificado.url, timeout=10)
                    if r.status_code == 200:
                        writer.append(io.BytesIO(r.content))
                except Exception:
                    pass

    anexar_certificados(cursos)
    anexar_certificados(reconocimientos)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="Portafolio_{perfil.apellidos}.pdf"'
    writer.write(response)
    writer.close()

    return response