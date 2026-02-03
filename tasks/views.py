# tasks/views.py - VERSIÓN CORREGIDA CON CAMPOS REALES
import datetime
from django.shortcuts import render
from django.http import HttpResponse

# Importar modelos
from .models import (
    DatosPersonales, ExperienciaLaboral, 
    CursoRealizado, Reconocimiento, 
    ProductoAcademico, ProductoLaboral, VentaGarage
)

# ========== FUNCIÓN AUXILIAR ==========
def get_perfil():
    """Obtiene perfil activo."""
    try:
        return DatosPersonales.objects.filter(perfilactivo=1).first()
    except:
        return None

# ========== VISTAS BÁSICAS ==========
def home(request):
    perfil = get_perfil()
    if not perfil:
        return render(request, 'home.html', {'perfil': None})
    
    context = {
        'perfil': perfil,
        'resumen_exp': ExperienciaLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )[:3],
        'resumen_cursos': CursoRealizado.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )[:3],
        'resumen_rec': Reconocimiento.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )[:3],
        'resumen_acad': ProductoAcademico.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )[:3],
        'resumen_lab': ProductoLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )[:3],
        'resumen_garage': VentaGarage.objects.all()[:5],
    }
    return render(request, 'home.html', context)

def experiencia(request):
    perfil = get_perfil()
    exp_list = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, 'experiencia.html', {
        'experiencias': exp_list, 
        'perfil': perfil
    })

def productos_academicos(request):
    perfil = get_perfil()
    prod_acad = ProductoAcademico.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, 'productos_academicos.html', {
        'productos_academicos': prod_acad, 
        'perfil': perfil
    })

def productos_laborales(request):
    perfil = get_perfil()
    prod_lab = ProductoLaboral.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, 'productos_laborales.html', {
        'productos_laborales': prod_lab, 
        'perfil': perfil
    })

def cursos(request):
    perfil = get_perfil()
    cursos_list = CursoRealizado.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, 'cursos.html', {
        'cursos': cursos_list, 
        'perfil': perfil
    })

def reconocimientos(request):
    perfil = get_perfil()
    reco_list = Reconocimiento.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, 'reconocimientos.html', {
        'reconocimientos': reco_list, 
        'perfil': perfil
    })

def garage(request):
    perfil = get_perfil()
    items = VentaGarage.objects.all()
    return render(request, 'garage.html', {
        'garage_items': items, 
        'perfil': perfil
    })

# ========== GENERAR PDF/HTML ==========
def exportar_cv(request):
    """Genera CV en formato imprimible usando CAMPOS REALES."""
    perfil = get_perfil()
    if not perfil:
        return HttpResponse("""
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2>No hay perfil activo</h2>
            <p><a href="/admin/">Configura un perfil</a></p>
            <p><a href="/">← Volver al inicio</a></p>
        </body>
        </html>
        """)
    
    # Usar campos REALES según tu admin.py
    nombres = perfil.nombres
    apellidos = perfil.apellidos
    
    # Para profesión: usar nacionalidad o texto genérico
    profesion = perfil.nacionalidad if perfil.nacionalidad else "Profesional"
    
    # Contacto - usar campos REALES
    telefono = perfil.telefonoconvencional if perfil.telefonoconvencional else ""
    direccion = perfil.direcciondomiciliaria if perfil.direcciondomiciliaria else ""
    perfil_profesional = perfil.descripcionperfil if perfil.descripcionperfil else ""
    
    # Obtener datos relacionados CON CAMPOS REALES
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
    
    cursos_list = CursoRealizado.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    )
    
    reconocimientos_list = Reconocimiento.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    )
    
    # Fecha actual
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # HTML para imprimir
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>CV - {nombres} {apellidos}</title>
        <style>
            /* ESTILOS PARA IMPRESIÓN */
            @media print {{
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: "Times New Roman", serif;
                    font-size: 12pt;
                    line-height: 1.5;
                    color: #000;
                    background: white !important;
                }}
                .no-print {{
                    display: none !important;
                }}
                h1, h2, h3 {{
                    page-break-after: avoid;
                }}
                .section {{
                    page-break-inside: avoid;
                }}
            }}
            
            /* ESTILOS PARA PANTALLA */
            @media screen {{
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f0f2f5;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .print-panel {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                    z-index: 1000;
                }}
                .btn {{
                    display: block;
                    width: 200px;
                    padding: 12px;
                    margin: 10px 0;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    cursor: pointer;
                    text-align: center;
                    text-decoration: none;
                }}
                .btn-print {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .btn-back {{
                    background: #6c757d;
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 3px solid #007bff;
                    margin-bottom: 30px;
                }}
                h1 {{
                    color: #2c3e50;
                    margin: 0;
                }}
                h2 {{
                    color: #3498db;
                    margin: 10px 0;
                }}
                .section-title {{
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 5px;
                    margin: 25px 0 15px 0;
                }}
                .item {{
                    margin: 15px 0;
                    padding: 15px;
                    background: #f8f9fa;
                    border-left: 4px solid #3498db;
                    border-radius: 0 5px 5px 0;
                }}
            }}
        </style>
    </head>
    <body>
        <!-- PANEL DE IMPRESIÓN -->
        <div class="print-panel no-print">
            <h3 style="margin-top: 0;">📄 Guardar como PDF</h3>
            <button onclick="window.print()" class="btn btn-print">
                🖨️ Imprimir / Guardar PDF
            </button>
            <a href="/" class="btn btn-back">← Volver al Inicio</a>
            <p style="font-size: 12px; color: #666; margin-top: 10px;">
                <strong>Instrucción:</strong><br>
                1. Click en "Imprimir"<br>
                2. Destino: "Microsoft Print to PDF"<br>
                3. ¡Listo!
            </p>
        </div>
        
        <!-- CONTENIDO DEL CV -->
        <div class="container">
            <!-- ENCABEZADO -->
            <div class="header">
                <h1>{nombres} {apellidos}</h1>
                <h2>{profesion}</h2>
                <p>📞 {telefono} | 📍 {direccion}</p>
                {"<p>🌐 " + perfil.sitioweb + "</p>" if perfil.sitioweb else ""}
                {"<p>📧 Correo: No disponible en el sistema</p>"}
            </div>
            
            <!-- PERFIL PROFESIONAL -->
            {f'<div class="section"><h3 class="section-title">Perfil Profesional</h3><p>{perfil_profesional}</p></div>' if perfil_profesional else ''}
            
            <!-- EXPERIENCIA LABORAL -->
            {f'<div class="section"><h3 class="section-title">Experiencia Laboral</h3>{"".join([f"""<div class="item"><h4 style="margin: 0; color: #2c3e50;">{exp.cargodesempenado}</h4><p style="margin: 5px 0; color: #7f8c8d;"><i>{exp.nombrempresa} | {exp.fechainiciogestion} - {exp.fechafingestion}</i></p><p>{exp.descripcion or ""}</p></div>""" for exp in experiencias])}</div>' if experiencias.exists() else ''}
            
            <!-- PRODUCTOS ACADÉMICOS -->
            {f'<div class="section"><h3 class="section-title">Productos Académicos</h3>{"".join([f"""<div class="item"><h4 style="margin: 0; color: #2c3e50;">{prod.nombrerecurso}</h4><p><strong>Clasificador:</strong> {prod.clasificador or ""}</p><p>{prod.descripcion or ""}</p></div>""" for prod in academicos])}</div>' if academicos.exists() else ''}
            
            <!-- PRODUCTOS LABORALES -->
            {f'<div class="section"><h3 class="section-title">Productos Laborales</h3>{"".join([f"""<div class="item"><h4 style="margin: 0; color: #2c3e50;">{prod.nombreproducto}</h4><p><strong>Fecha:</strong> {prod.fechaproducto}</p><p>{prod.descripcion or ""}</p></div>""" for prod in laborales])}</div>' if laborales.exists() else ''}
            
            <!-- CURSOS -->
            {f'<div class="section"><h3 class="section-title">Cursos Realizados</h3>{"".join([f"""<div class="item"><h4 style="margin: 0; color: #2c3e50;">{curso.nombrecurso}</h4><p style="margin: 5px 0; color: #7f8c8d;"><i>{curso.entidadpatrocinadora} | {curso.fechafin} | {curso.totalhoras} horas</i></p></div>""" for curso in cursos_list])}</div>' if cursos_list.exists() else ''}
            
            <!-- RECONOCIMIENTOS -->
            {f'<div class="section"><h3 class="section-title">Reconocimientos</h3>{"".join([f"""<div class="item"><h4 style="margin: 0; color: #2c3e50;">{rec.descripcionreconocimiento}</h4><p style="margin: 5px 0; color: #7f8c8d;"><i>{rec.tiporeconocimiento} | {rec.fechareconocimiento}</i></p><p>{rec.descripcion or ""}</p></div>""" for rec in reconocimientos_list])}</div>' if reconocimientos_list.exists() else ''}
            
            <!-- INFORMACIÓN ADICIONAL -->
            <div class="section">
                <h3 class="section-title">Información Personal</h3>
                <div class="item">
                    <p><strong>Nacionalidad:</strong> {perfil.nacionalidad or "No especificada"}</p>
                    {f'<p><strong>Lugar de nacimiento:</strong> {perfil.lugarnacimiento}</p>' if perfil.lugarnacimiento else ''}
                    {f'<p><strong>Fecha de nacimiento:</strong> {perfil.fechanacimiento}</p>' if perfil.fechanacimiento else ''}
                    {f'<p><strong>Cédula:</strong> {perfil.numerocedula}</p>' if perfil.numerocedula else ''}
                    {f'<p><strong>Estado civil:</strong> {perfil.estadocivil}</p>' if perfil.estadocivil else ''}
                </div>
            </div>
            
            <!-- PIE DE PÁGINA -->
            <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 11px;">
                <p>Documento generado el {fecha}</p>
                <p>CV profesional de {nombres} {apellidos}</p>
            </div>
        </div>
        
        <script>
            // Auto-imprimir después de 2 segundos
            setTimeout(() => {{
                if (!sessionStorage.getItem('alreadyPrinted')) {{
                    window.print();
                    sessionStorage.setItem('alreadyPrinted', 'true');
                }}
            }}, 2000);
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(html)

def pdf_datos_personales(request):
    """Alias para mantener compatibilidad."""
    return exportar_cv(request)