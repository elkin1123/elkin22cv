# tasks/views.py - VERSIÓN DEFINITIVA PARA RENDER
import datetime
from django.shortcuts import render
from django.http import HttpResponse

# Importar modelos
from .models import (
    DatosPersonales, ExperienciaLaboral, 
    CursoRealizado, Reconocimiento, 
    ProductoAcademico, ProductoLaboral, VentaGarage
)

# ========== FUNCIÓN AUXILIAR SEGURA ==========
def get_perfil():
    """Obtiene perfil activo de forma segura."""
    try:
        return DatosPersonales.objects.filter(perfilactivo=1).first()
    except:
        try:
            return DatosPersonales.objects.first()
        except:
            return None

# ========== VISTAS SEGURAS CON TRY/EXCEPT ==========
def home(request):
    try:
        perfil = get_perfil()
        if not perfil:
            # Crear perfil automático si no existe
            try:
                perfil = DatosPersonales.objects.create(
                    nombres="Elkin Joshua",
                    apellidos="Delgado López",
                    descripcionperfil="Desarrollador Web | Estudiante de TI",
                    perfilactivo=1,
                    nacionalidad="Ecuatoriano",
                    numerocedula="1316712379",
                    telefonoconvencional="---",
                    direcciondomiciliaria="Calle 5 de mayo",
                    sitioweb="https://github.com/elkinl123"
                )
            except:
                perfil = None
        
        # Inicializar listas vacías
        experiencias = []
        cursos = []
        reconocimientos = []
        academicos = []
        laborales = []
        garage_items = []
        
        if perfil:
            try:
                experiencias = ExperienciaLaboral.objects.filter(
                    idperfilconqueestaactivo=perfil
                )[:3]
            except:
                experiencias = []
                
            try:
                cursos = CursoRealizado.objects.filter(
                    idperfilconqueestaactivo=perfil
                )[:3]
            except:
                cursos = []
                
            try:
                reconocimientos = Reconocimiento.objects.filter(
                    idperfilconqueestaactivo=perfil
                )[:3]
            except:
                reconocimientos = []
                
            try:
                academicos = ProductoAcademico.objects.filter(
                    idperfilconqueestaactivo=perfil
                )[:3]
            except:
                academicos = []
                
            try:
                laborales = ProductoLaboral.objects.filter(
                    idperfilconqueestaactivo=perfil
                )[:3]
            except:
                laborales = []
        
        # Garage siempre se intenta cargar
        try:
            garage_items = VentaGarage.objects.all()[:5]
        except:
            # Si falla, usar datos de ejemplo
            garage_items = [
                {'nombreproducto': 'Producto 1', 'valordelbien': 100, 'estadoproducto': 'Disponible'},
                {'nombreproducto': 'Producto 2', 'valordelbien': 200, 'estadoproducto': 'Disponible'},
            ]
        
        context = {
            'perfil': perfil,
            'resumen_exp': experiencias,
            'resumen_cursos': cursos,
            'resumen_rec': reconocimientos,
            'resumen_acad': academicos,
            'resumen_lab': laborales,
            'resumen_garage': garage_items,
        }
        return render(request, 'home.html', context)
        
    except Exception as e:
        # Vista de fallback si todo falla
        return render(request, 'home.html', {
            'perfil': None,
            'error': f"Error: {str(e)}"
        })

def experiencia(request):
    try:
        perfil = get_perfil()
        exp_list = []
        if perfil:
            # Intentar varios nombres de campo posibles
            try:
                exp_list = ExperienciaLaboral.objects.filter(
                    idperfilconqueestaactivo=perfil
                )
            except:
                # Si falla, intentar sin filtro
                exp_list = ExperienciaLaboral.objects.all()
        return render(request, 'experiencia.html', {
            'experiencias': exp_list, 
            'perfil': perfil
        })
    except:
        return render(request, 'experiencia.html', {
            'experiencias': [],
            'perfil': None
        })

def productos_academicos(request):
    try:
        perfil = get_perfil()
        prod_acad = []
        if perfil:
            try:
                prod_acad = ProductoAcademico.objects.filter(
                    idperfilconqueestaactivo=perfil
                )
            except:
                prod_acad = ProductoAcademico.objects.all()
        return render(request, 'productos_academicos.html', {
            'productos_academicos': prod_acad, 
            'perfil': perfil
        })
    except:
        return render(request, 'productos_academicos.html', {
            'productos_academicos': [],
            'perfil': None
        })

def productos_laborales(request):
    try:
        perfil = get_perfil()
        prod_lab = []
        if perfil:
            try:
                prod_lab = ProductoLaboral.objects.filter(
                    idperfilconqueestaactivo=perfil
                )
            except:
                prod_lab = ProductoLaboral.objects.all()
        return render(request, 'productos_laborales.html', {
            'productos_laborales': prod_lab, 
            'perfil': perfil
        })
    except:
        return render(request, 'productos_laborales.html', {
            'productos_laborales': [],
            'perfil': None
        })

def cursos(request):
    try:
        perfil = get_perfil()
        cursos_list = []
        if perfil:
            try:
                cursos_list = CursoRealizado.objects.filter(
                    idperfilconqueestaactivo=perfil
                )
            except:
                cursos_list = CursoRealizado.objects.all()
        return render(request, 'cursos.html', {
            'cursos': cursos_list, 
            'perfil': perfil
        })
    except:
        return render(request, 'cursos.html', {
            'cursos': [],
            'perfil': None
        })

def reconocimientos(request):
    try:
        perfil = get_perfil()
        reco_list = []
        if perfil:
            try:
                reco_list = Reconocimiento.objects.filter(
                    idperfilconqueestaactivo=perfil
                )
            except:
                reco_list = Reconocimiento.objects.all()
        return render(request, 'reconocimientos.html', {
            'reconocimientos': reco_list, 
            'perfil': perfil
        })
    except:
        return render(request, 'reconocimientos.html', {
            'reconocimientos': [],
            'perfil': None
        })

def garage(request):
    try:
        perfil = get_perfil()
        items = []
        try:
            items = VentaGarage.objects.all()
        except:
            # Si falla, crear datos de ejemplo
            items = [
                type('obj', (object,), {
                    'nombreproducto': 'Producto Ejemplo 1',
                    'estadoproducto': 'Disponible',
                    'valordelbien': 50.00,
                    'descripcion': 'Descripción del producto'
                })(),
                type('obj', (object,), {
                    'nombreproducto': 'Producto Ejemplo 2',
                    'estadoproducto': 'Vendido',
                    'valordelbien': 75.00,
                    'descripcion': 'Otra descripción'
                })(),
            ]
        return render(request, 'garage.html', {
            'garage_items': items, 
            'perfil': perfil
        })
    except Exception as e:
        return render(request, 'garage.html', {
            'garage_items': [],
            'perfil': None,
            'error': str(e)
        })

# ========== GENERAR PDF/HTML ==========
def exportar_cv(request):
    """Genera CV en formato imprimible."""
    try:
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
        
        # Obtener datos (con try/except para cada uno)
        try:
            experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil)
        except:
            experiencias = []
            
        try:
            academicos = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil)
        except:
            academicos = []
            
        try:
            laborales = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil)
        except:
            laborales = []
            
        try:
            cursos_list = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil)
        except:
            cursos_list = []
            
        try:
            reconocimientos_list = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil)
        except:
            reconocimientos_list = []
        
        # Fecha actual
        fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # HTML para imprimir
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>CV - {perfil.nombres} {perfil.apellidos}</title>
            <style>
                @media print {{
                    @page {{ margin: 2cm; }}
                    body {{ font-family: "Times New Roman", serif; font-size: 12pt; }}
                    .no-print {{ display: none !important; }}
                }}
                @media screen {{
                    body {{ font-family: Arial; margin: 20px; background: #f0f2f5; }}
                    .container {{ max-width: 800px; margin: auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                    .print-panel {{ position: fixed; top: 20px; right: 20px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); z-index: 1000; }}
                    .btn {{ display: block; width: 200px; padding: 12px; margin: 10px 0; background: #007bff; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; text-align: center; }}
                    .header {{ text-align: center; padding-bottom: 20px; border-bottom: 3px solid #007bff; margin-bottom: 30px; }}
                    .section-title {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin: 25px 0 15px 0; }}
                    .item {{ margin: 15px 0; padding: 15px; background: #f8f9fa; border-left: 4px solid #3498db; border-radius: 0 5px 5px 0; }}
                }}
            </style>
        </head>
        <body>
            <div class="print-panel no-print">
                <h3>📄 Guardar como PDF</h3>
                <button onclick="window.print()" class="btn">🖨️ Imprimir / Guardar PDF</button>
                <a href="/" class="btn" style="background: #6c757d;">← Volver al Inicio</a>
            </div>
            
            <div class="container">
                <div class="header">
                    <h1>{perfil.nombres} {perfil.apellidos}</h1>
                    <h2>{perfil.nacionalidad if perfil.nacionalidad else 'Profesional'}</h2>
                    <p>📞 {perfil.telefonoconvencional if perfil.telefonoconvencional else ''} | 📍 {perfil.direcciondomiciliaria if perfil.direcciondomiciliaria else ''}</p>
                    {f'<p>🌐 {perfil.sitioweb}</p>' if perfil.sitioweb else ''}
                </div>
                
                {f'<div class="section"><h3 class="section-title">Perfil Profesional</h3><p>{perfil.descripcionperfil}</p></div>' if perfil.descripcionperfil else ''}
                
                {f'<div class="section"><h3 class="section-title">Experiencia Laboral</h3>{"".join([f"<div class=\"item\"><h4>{exp.cargodesempenado}</h4><p><i>{getattr(exp, 'nombrempresa', '')} | {getattr(exp, 'fechainiciogestion', '')} - {getattr(exp, 'fechafingestion', '')}</i></p><p>{getattr(exp, 'descripcion', '')}</p></div>" for exp in experiencias])}</div>' if experiencias else ''}
                
                {f'<div class="section"><h3 class="section-title">Productos Académicos</h3>{"".join([f"<div class=\"item\"><h4>{prod.nombrerecurso}</h4><p>{getattr(prod, 'clasificador', '')}</p><p>{getattr(prod, 'descripcion', '')}</p></div>" for prod in academicos])}</div>' if academicos else ''}
                
                {f'<div class="section"><h3 class="section-title">Productos Laborales</h3>{"".join([f"<div class=\"item\"><h4>{prod.nombreproducto}</h4><p>{getattr(prod, 'fechaproducto', '')}</p><p>{getattr(prod, 'descripcion', '')}</p></div>" for prod in laborales])}</div>' if laborales else ''}
                
                {f'<div class="section"><h3 class="section-title">Cursos Realizados</h3>{"".join([f"<div class=\"item\"><h4>{curso.nombrecurso}</h4><p><i>{getattr(curso, 'entidadpatrocinadora', '')} | {getattr(curso, 'fechafin', '')} | {getattr(curso, 'totalhoras', '')} horas</i></p></div>" for curso in cursos_list])}</div>' if cursos_list else ''}
                
                {f'<div class="section"><h3 class="section-title">Reconocimientos</h3>{"".join([f"<div class=\"item\"><h4>{rec.descripcionreconocimiento}</h4><p><i>{getattr(rec, 'tiporeconocimiento', '')} | {getattr(rec, 'fechareconocimiento', '')}</i></p><p>{getattr(rec, 'descripcion', '')}</p></div>" for rec in reconocimientos_list])}</div>' if reconocimientos_list else ''}
                
                <div class="section">
                    <h3 class="section-title">Información Personal</h3>
                    <div class="item">
                        <p><strong>Nacionalidad:</strong> {perfil.nacionalidad or 'No especificada'}</p>
                        {f'<p><strong>Cédula:</strong> {perfil.numerocedula}</p>' if perfil.numerocedula else ''}
                        {f'<p><strong>Estado civil:</strong> {perfil.estadocivil}</p>' if perfil.estadocivil else ''}
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 11px;">
                    <p>Documento generado el {fecha}</p>
                    <p>CV profesional de {perfil.nombres} {perfil.apellidos}</p>
                </div>
            </div>
            
            <script>
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
        
    except Exception as e:
        return HttpResponse(f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2>Error generando CV</h2>
            <p>{str(e)}</p>
            <p><a href="/">← Volver al inicio</a></p>
        </body>
        </html>
        """)

def pdf_datos_personales(request):
    """Alias para mantener compatibilidad."""
    return exportar_cv(request)