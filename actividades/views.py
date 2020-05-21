from django.urls import reverse_lazy
from .models import Actividad, Programa
from django.shortcuts import get_object_or_404, redirect
from . import forms
from django.views.generic.edit import (
    CreateView, UpdateView,
)
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages


class ListaActividadPDF(ListView):
    model = Actividad


class NuevaActividad(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('actividades.add_subprograma')
    login_url = 'usuarios/login/'
    success_message = "Actividad agregada exitosamente"
    model = Actividad
    form_class = forms.ActividadForm
    success_url = reverse_lazy('lista_actividades')


class ProgramaNuevaActividad(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('actividades.add_subprograma')
    login_url = 'usuarios/login/'
    success_message = "Actividad agregada exitosamente"
    model = Actividad
    form_class = forms.ActividadForm

    def get_context_data(self, **kwargs):
        self.programa = get_object_or_404(Programa, pk=self.kwargs['progPk'])
        context = super().get_context_data(**kwargs)
        context['programa'] = self.programa
        return context

    def get_success_url(self):
        self.programa = get_object_or_404(Programa, pk=self.kwargs['progPk'])
        return reverse_lazy('lista_programa_actividades', kwargs={'pk': self.programa.id})


class ListaActividades(PermissionRequiredMixin, ListView):
    permission_required = ('actividades.view_subprograma')
    login_url = 'usuarios/login/'
    model = Actividad
    paginate_by = 10
    ordering = ['programa']


class ListaProgramaActividades(ListView):
    permission_required = ('actividades.view_subprograma')
    login_url = 'usuarios/login/'
    paginate_by = 10

    def get_queryset(self):
        self.programa = get_object_or_404(Programa, pk=self.kwargs['pk'])
        return Actividad.objects.filter(programa=self.programa)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programa'] = self.programa
        return context


class VerActividad(PermissionRequiredMixin, DetailView):
    permission_required = ('actividades.view_subprograma')
    login_url = 'usuarios/login/'
    model = Actividad


class ProgramaVerActividad(PermissionRequiredMixin, DetailView):
    permission_required = ('actividades.view_subprograma')
    login_url = 'usuarios/login/'
    model = Actividad

    def get_context_data(self, **kwargs):
        self.programa = get_object_or_404(Programa, pk=self.kwargs['progPk'])
        context = super().get_context_data(**kwargs)
        context['programa'] = self.programa
        return context


class EditarActividad(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('actividades.change_subprograma')
    login_url = 'usuarios/login/'
    form_class = forms.EdicionActividadForm
    model = Actividad
    success_message = "Datos de la Actividad modificados correctamente"
    success_url = reverse_lazy('lista_actividades')


class ProgramaEditarActividad(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('actividades.change_subprograma')
    login_url = 'usuarios/login/'
    form_class = forms.EdicionActividadForm
    model = Actividad
    success_message = "Datos de la Actividad modificados correctamente"
    success_url = reverse_lazy('lista_actividades')

    def get_context_data(self, **kwargs):
        self.programa = get_object_or_404(Programa, pk=self.kwargs['progPk'])
        context = super().get_context_data(**kwargs)
        context['programa'] = self.programa
        return context

    def get_success_url(self):
        self.programa = get_object_or_404(Programa, pk=self.kwargs['progPk'])
        return reverse_lazy('lista_programa_actividades', kwargs={'pk': self.programa.id})


def desactivar_actividad(request, id):
    messages.add_message(request, 10, cambia_estatus_act('INA', id))
    return redirect('lista_actividades')


def reactivar_actividad(request, id):
    messages.add_message(request, 10, cambia_estatus_act('ACT', id))
    return redirect('lista_actividades')


def desactivar_programa_actividad(request, progPk, id):
    messages.add_message(request, 10, cambia_estatus_act('INA', id))
    return redirect('lista_programa_actividades',  progPk)


def reactivar_programa_actividad(request, progPk, id):
    messages.add_message(request, 10, cambia_estatus_act('ACT', id))
    return redirect('lista_programa_actividades',  progPk)

def cambia_estatus_act(estatus,id):
    actividad = Actividad.objects.get(pk=id)
    actividad.estatus = estatus
    actividad.save()
    mensaje = 'Actividad "'+actividad.nombre+'" reactivada con éxito'
    return mensaje