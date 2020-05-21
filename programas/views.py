from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from .models import Programa, Partida, MetaPrograma, MetaReal, Inversion
from .forms import ProgramaForm, PartidaForm, MetaForm, MetaRealForm, InversionForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import ListView

class NuevoPrograma(SuccessMessageMixin, CreateView):
    model = Programa
    form_class = ProgramaForm
    success_url = reverse_lazy('lista_programa')
    success_message = "Programa creado con éxito"
    extra_context = {'inversion_form': InversionForm(),
                     'metas_esperadas_form': MetaForm(),
                     'metas_reales_form': MetaRealForm(),}
    template_name = 'programas/programa_form.html'

    def form_valid(self, form):
        inversion_form = InversionForm(self.request.POST)
        metas_esperadas_form = MetaForm(self.request.POST, )
        metas_reales_form = MetaRealForm(self.request.POST, )
        
        if (form.is_valid() and inversion_form.is_valid() and metas_esperadas_form.is_valid()
                and metas_reales_form.is_valid()):  # Añadir más forms aquí
            programa = form.save(commit=False)
            programa.save()

            inversion = inversion_form.save(commit=False)
            inversion.programa_inversion = programa
            inversion.save()

            metas_esperadas = metas_esperadas_form.save(commit=False)
            metas_esperadas.programa = programa
            metas_esperadas.meta_esperada = True
            metas_esperadas.save()

            metas_reales = metas_reales_form.save(commit=False)
            metas_reales.programa_r = programa
            metas_reales.meta_esperada_r = False
            metas_reales.save()

        else:
            return render(self.request, 'programas/programa_form.html',{'form':form, 'inversion_form': inversion_form,
            'metas_esperadas_form': metas_esperadas_form, 'metas_reales_form': metas_reales_form})
            #return self.render_to_response(self.get_context_data(form=form,
            #                               extra_context={
            #                                              inversion_form,
            #                                              metas_esperadas_form,
            #                                              metas_reales_form}))

        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        inversion_form = InversionForm(self.request.POST)
        metas_esperadas_form = MetaForm(self.request.POST)
        metas_reales_form = MetaRealForm(self.request.POST)
        #return self.render_to_response(self.get_context_data(form=form,
        #                               extra_context={
        #                                             inversion_form,
        #                                              metas_esperadas_form,
        #                                              metas_reales_form}))
        return render(self.request, 'programas/programa_form.html', {'form':form, 'inversion_form': inversion_form,
            'metas_esperadas_form': metas_esperadas_form, 'metas_reales_form': metas_reales_form})

    def get_context_data(self, **kwargs):
        if 'extra_context' in kwargs:
            lista = list(kwargs['extra_context'])
            self.extra_context = {
                'inversion_form': lista[0],
                'metas_esperadas_form': lista[1],
                'metas_reales_form': lista[2]}
        return super().get_context_data(**kwargs)


class ActualizaPrograma(UpdateView):
    model = Programa
    form_class = ProgramaForm
    template_name = 'programas/programa_edit.html'
    success_url = reverse_lazy('lista_programa')


def editar_programa(request, id):
    programa = Programa.objects.get(pk=id)
    inversion = Inversion.objects.get(programa_inversion=id)
    metas_esperadas = MetaPrograma.objects.get(programa=id)
    metas_reales = MetaReal.objects.get(programa_r=id)

    if request.method == 'POST':

        programa_form = ProgramaForm(data=request.POST, instance=programa)
        inversion_form = InversionForm(data=request.POST, instance=inversion)
        metas_esperadas_form = MetaForm(
            data=request.POST, instance=metas_esperadas)
        metas_reales_form = MetaRealForm(
            data=request.POST, instance=metas_reales)

        if (programa_form.is_valid() and inversion_form.is_valid()
                and metas_reales_form.is_valid()
                and metas_esperadas_form.is_valid()):
            programa_f = programa_form.save(commit=False)
            programa_f.save()

            inversion_f = inversion_form.save(commit=False)
            
            inversion_f.save()

            metas_esperadas_f = metas_esperadas_form.save(commit=False)
            metas_esperadas_f.save()

            metas_reales_f = metas_reales_form.save(commit=False)
            metas_reales_f.save()
            messages.success(request, 'Programa modificado exitosamente.')
            return redirect('lista_programa')
    else:
        programa_form = ProgramaForm(instance=programa)
        inversion_form = InversionForm(instance=inversion)
        metas_esperadas_form = MetaForm(instance=metas_esperadas)
        metas_reales_form = MetaRealForm(instance=metas_reales)

    return render(request, 'programas/programa_edit.html', {
        'programa_form': programa_form,
        'inversion_form' : inversion_form,
        'metas_esperadas_form': metas_esperadas_form,
        'metas_reales_form': metas_reales_form
    })


class ListaPrograma(ListView):
    model = Programa
    paginate_by = 10
    ordering = ['nombre']


def desactivar_programa(request, id):
    programa = Programa.objects.get(pk=id)
    if programa.status.upper() == 'ACT':
        programa.status = 'INA'
        programa.save()
        messages.success(
            request, 'Programa seleccionado se ha desactivado con éxito')
        return redirect('lista_programa')
    mensaje = 'No fue posible desactivar el programa en este momento,'
    mensaje += ' debido a un error interno. Favor de intentarlo más tarde.'
    messages.success(
        request,
        mensaje)
    return redirect('lista_programa')


def reactivar_programa(request, id):
    programa = Programa.objects.get(pk=id)
    if programa.status.upper() != 'ACT':
        programa.status = 'ACT'
        programa.save()
        messages.success(request, 'Programa seleccionado reactivado con éxito')
        return redirect('lista_programa')
    mensaje = 'No fue posible reactivar el programa en este momento,'
    mensaje += ' debido a un error interno. Favor de intentarlo más tarde.'
    messages.success(
        request, mensaje)
    return redirect('lista_programa')

