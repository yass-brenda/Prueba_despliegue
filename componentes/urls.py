from django.urls import path
from . import views
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    path('nuevo', permission_required('componentes.add_componentes')
         (views.NuevoComponente.as_view()),
         name='nuevo_componentes'),
    path('', permission_required('componentes.view_componentes')
         (views.ListaComponentes.as_view()),
         name='lista_componentes'),
    path('actividades/<int:id>',
         permission_required('componentes.view_actividades')
         (views.lista_actividad),
         name='lista_actividad'),
    path('desactivar/<int:id>', permission_required('componentes.view_componentes')
         (views.DesactivarComponentes),
         name='desactivar_componentes'),
    path('activar/<int:id>', permission_required('componentes.view_componentes')
         (views.ReactivarComponente),
         name='activar_componentes'),
    path('nuevaActividades/<int:id>', permission_required('componentes.add_actividades')
         (views.agregar_actividad),
         name='agregar_actividad'),
    path('editar/<int:id>', permission_required('componentes.change_componentes')
         (views.editar_componente),
         name='editar_componentes'),

]
