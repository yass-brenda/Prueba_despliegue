from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Administrativo
from .forms import UserForm, LoginForm, AdministrativoForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.core.paginator import Paginator


class NuevoUsuario(PermissionRequiredMixin, CreateView):
    permission_required = ('auth.add_user')
    login_url = 'usuarios/login/'
    model = User
    form_class = UserForm
    extra_context = {'administrativo_form': AdministrativoForm()}
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('lista_usuarios')

    def form_valid(self, form):
        administrativo_form = AdministrativoForm(
            self.request.POST, self.request.FILES)
        if administrativo_form.is_valid() and form.is_valid():
            user = form.save(commit=False)
            user.save()
            if user.is_superuser:
                group = Group.objects.get(name='director_operativo')
            else:
                group = Group.objects.get(name='encargado_subprograma')
            user.groups.add(group)
            administrativo = administrativo_form.save(commit=False)
            administrativo.usuario = user
            administrativo.save()
        else:
            return render(self.request, 'usuarios/usuario_form.html', {'admin': administrativo_form, 'form':form})

        self.object = form.save()
        messages.success(
            self.request, 'Cuenta creada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        administrativo_form = AdministrativoForm(self.request.POST, self.request.FILES)
        return render(self.request, 'usuarios/usuario_form.html', {'admin': administrativo_form, 'form':form})


    def get_context_data(self, **kwargs):
        if 'extra_context' in kwargs:
            self.extra_context = {
                'administrativo_form': kwargs['extra_context']}
        return super().get_context_data(**kwargs)


class ListaUsuarios(PermissionRequiredMixin, ListView):
    permission_required = ('auth.view_user')
    login_url = 'usuarios/login/'
    model = Administrativo
    template_name = 'usuarios/usuarios.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        administrativos = Administrativo.objects.all()
        admins = []
        for admin in administrativos:
            admins.append({'admin': admin, 'usuario': admin.usuario})

        self.object_list = admins
        context = self.get_context_data()
        
        paginator = Paginator(admins, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        #return self.render_to_response(context)
        return render(self.request, 'usuarios/usuarios.html', {'page_obj': page_obj})


class Login(LoginView):
    template_name = "usuarios/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('lista_usuarios')


def editar_usuario(request, id):
    administrativo = Administrativo.objects.get(usuario=id)
    if request.method == 'POST':
        admin_form = AdministrativoForm(
            data=request.POST, instance=administrativo)
        if admin_form.is_valid():
            admin_form.save()
            messages.success(
                request, 'Perfil de usuario modificado exitosamente.')
            return redirect('lista_usuarios')
    else:
        admin_form = AdministrativoForm(instance=administrativo)
    return render(
        request, 'usuarios/editar_usuario.html', {'admin': administrativo})


@permission_required('auth.view_user')
def desactivar_usuario(request, id):
    user = User.objects.get(pk=id)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request, 'Cuenta desactivada con éxito.')
        return redirect('lista_usuarios')
    messages.success(
        request, 'No es posible desactivar la cuenta. Intente más tarde.')
    return redirect('lista_usuarios')


@permission_required('auth.view_user')
def activar_usuario(request, id):
    user = User.objects.get(pk=id)
    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, 'Cuenta activada con éxito.')
        return redirect('lista_usuarios')
    messages.success(
        request, 'No es posible activar la cuenta. Intente más tarde.')
    return redirect('lista_usuarios')
