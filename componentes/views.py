
from django.shortcuts import render, redirect
from .models import Componentes, Actividades
from .forms import ComponenteForm, ActividadesForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator

# Create your views here.


class NuevoComponente(PermissionRequiredMixin, CreateView):
    permission_required = ('componentes.add_componentes')
    login_url = 'usuarios/login/'
    model = Componentes
    form_class = ComponenteForm
    success_url = reverse_lazy('lista_componentes')
    #extra_context = {'actividad_form': ActividadesForm()}
    #template_name = 'componentes/componentes_form.html'

    '''def form_valid(self, form):
        actividad_form = ActividadesForm(self.request.POST, self.request.FILES)
        print(actividad_form)
        if actividad_form.is_valid():
            componentes = form.save(commit=False)
            componentes.is_active = False
            componentes.save()

            actividad = actividad_form.save(commit=False)
            actividad.componente = componentes
            actividad.save()
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form, extra_context=actividad_form))
        return super().form_valid(form)

    def form_invalid(self, form):
        actividad_form = ActividadesForm(self.request.POST, self.request.FILES)
        return self.render_to_response(
            self.get_context_data(
                form=form,
                extra_context=actividad_form))

    def get_context_data(self, **kwargs):
        if 'extra_context' in kwargs:
            self.extra_context = {'actividad_form': kwargs['extra_context']}
        return super().get_context_data(**kwargs)'''


@permission_required('componentes.view_componentes')
def DesactivarComponentes(request, id):
    componentes = Componentes.objects.get(pk=id)
    if componentes.activo:
        componentes.activo = False
        componentes.save()
        messages.success(request, 'Proyecto desactivado con exito.')
        return redirect('lista_componentes')
    messages.success(request, 'No es posible desactivar el proyecto')
    return redirect('lista_componentes')


@permission_required('componentes.view_componentes')
def ReactivarComponente(request, id):
    componentes = Componentes.objects.get(pk=id)
    if not componentes.activo:
        componentes.activo = True
        componentes.save()
        messages.success(request, 'Componente activado con exito.')
        return redirect('lista_componentes')
    messages.success(request, 'No es posible activar el componente')
    return redirect('lista_componentes')


@permission_required('componentes.change_componentes')
def editar_componente(request, id):
    componentes = Componentes.objects.get(pk=id)
    if request.method == 'POST':
        componentes_form = ComponenteForm(data=request.POST, instance=componentes)
        if componentes_form.is_valid():
            componentes_form.save()
            messages.success(request, 'Componente modificado con exito.')
            return redirect('lista_componentes')
    else:
        componentes_form = ComponenteForm(instance=componentes)
    return render(request, 'componentes/componentes_edit.html', {
        'componentes_form': componentes_form,
    })


class ListaComponentes(PermissionRequiredMixin, ListView):
    permission_required = ('componentes.view_componentes')
    login_url = 'usuarios/login/'
    model = Componentes
    paginate_by = 5
    
@permission_required('componentes.add_actividades')
def agregar_actividad(request,id):
    if request.method == 'POST':
        form = ActividadesForm(request.POST)
        id = request.POST.get('id_componentes')
        print(id)
        if form.is_valid():
            actividad = form.save(commit=False)
            componente = Componentes.objects.get(id=id)
            actividad.componente = componente
            actividad.save()
            return redirect('lista_actividad',id)
    else:
        form = ActividadesForm()
    return render(request, 'actividad/nuevo.html', {'form': form, 'id':id})


@permission_required('componentes.view_actividades')
def lista_actividad(request, id):
    Componentes.objects.get(pk=id)
    actividad = Actividades.objects.filter(componente=id)
    context = {'actividades': actividad, 'id':id}
    
    

        
    page_number  = request.GET.get('page', 1)

    paginator = Paginator(actividad, 5)
    page=paginator.get_page(page_number)
    diccionario = {
        'actividades': page.object_list.all(),
        'page': page,
        'id': id
    }

    return render(request, 'actividad/actividades_list.html', diccionario)



