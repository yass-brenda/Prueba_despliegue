from django.urls import path
from . import views
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    path('nueva', permission_required('actividades.add_subprograma')(
        views.NuevaActividad.as_view()), name="nueva_actividad"),
    path('nueva/<int:progPk>', permission_required('actividades.add_subprograma')(
        views.ProgramaNuevaActividad.as_view()), name="nueva_programa_actividad"),

    path('', permission_required('actividades.view_subprograma')(
        views.ListaActividades.as_view()), name="lista_actividades"),
    path('programa/<int:pk>',
         views.ListaProgramaActividades.as_view(), name="lista_programa_actividades"),

    path('editar/<int:pk>',
         permission_required('actividades.change_subprograma')
         (views.EditarActividad.as_view()),
         name="editar_actividad"),
    path('editar/<int:progPk>/<int:pk>',
         permission_required('actividades.change_subprograma')
         (views.ProgramaEditarActividad.as_view()),
         name="editar_programa_actividad"),

    path(
        'ver/<int:pk>',
        permission_required('actividades.view_subprograma')(
            views.VerActividad.as_view()),
        name="ver_actividad"),
    path(
        'ver/<int:progPk>/<int:pk>',
        permission_required('actividades.view_subprograma')(
            views.ProgramaVerActividad.as_view()),
        name="ver_programa_actividad"),

    path('desactivar/<int:id>', views.desactivar_actividad,
         name='desactivar_actividad'),
    path('reactivar/<int:id>', views.reactivar_actividad,
         name='reactivar_actividad'),

    path('desactivarProgramaActividad/<int:progPk>/<int:id>', views.desactivar_programa_actividad,
         name='desactivar_programa_actividad'),
    path('reactivarProgramaActividad/<int:progPk>/<int:id>', views.reactivar_programa_actividad,
         name='reactivar_programa_actividad'),
]