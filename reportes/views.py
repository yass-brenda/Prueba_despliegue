from actividades.models import Actividad
from programas.models import Programa
from componentes.models import Componentes
from django.views.generic import ListView, TemplateView
from django_weasyprint import WeasyTemplateResponseMixin
from django.conf import settings


class EscogeReporte(TemplateView):
    template_name = "reportes/reportes.html"
    modulos = [
        {'tipo_modulo': 'Programas', 'url_name': 'programa_lista_pdf'},
        {'tipo_modulo': 'Actividades', 'url_name': 'actividades_lista_pdf'},
        {'tipo_modulo': 'Componentes', 'url_name': 'componentes_lista_pdf'}, ]
    extra_context = {'modulos': modulos}


# --------------------------------SUBPROGRAMAS
class ListaActividadPDF(ListView):
    model = Actividad
    template_name = 'reportes/ListaActividadesPDF.html'


class ActividadesPDF(WeasyTemplateResponseMixin, ListaActividadPDF):
    pdf_stylesheets = [
        settings.STATICFILES_DIRS[0] + 'css/bootstrap.min.css',
    ]
    pdf_attachment = False
    pdf_filename = 'actividades.pdf'


# --------------------------------PROGRAMAS
class ListaProgramaPDF(ListView):
    model = Programa
    template_name = 'reportes/ListaProgramaPDF.html'


class ProgramasPDF(WeasyTemplateResponseMixin, ListaProgramaPDF):
    pdf_stylesheets = [
        settings.STATICFILES_DIRS[0] + 'css/bootstrap.min.css',
    ]
    pdf_attachment = False
    pdf_filename = 'programas.pdf'


# --------------------------------PROYECTOS
class ListaComponentesPDF(ListView):
    model = Componentes
    template_name = 'reportes/ListaComponentesPDF.html'


class ComponentesPDF(WeasyTemplateResponseMixin, ListaComponentesPDF):
    pdf_stylesheets = [
        settings.STATICFILES_DIRS[0] + 'css/bootstrap.min.css',
    ]
    pdf_attachment = False
    pdf_filename = 'componentes.pdf'
