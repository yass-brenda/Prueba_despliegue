from django.urls import path
from reportes import views

urlpatterns = [
    path('', views.EscogeReporte.as_view(), name="escoge_reporte"),
    path('actividades_lista_pdf', views.ActividadesPDF.as_view(),
         name="actividades_lista_pdf"),
    path('programa_lista_pdf', views.ProgramasPDF.as_view(),
         name="programa_lista_pdf"),
    path('componentes_lista_pdf', views.ComponentesPDF.as_view(),
         name="componentes_lista_pdf"),
]
