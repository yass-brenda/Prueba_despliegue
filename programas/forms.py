#from .models import (Programa, Partida, MetaPrograma,
from .models import (Programa, Partida, MetaPrograma, Inversion,
                     MetaReal, LONGITUD_MAXIMA,
                     FORMATO_NUMERO_INCORRECTO)
from django.forms import ModelForm, TextInput, Select, NumberInput, ValidationError


class ProgramaForm(ModelForm):

    
    
    class Meta:
        model = Programa
        fields = "__all__"
        mensaje = 'El formato del recurso asignado es incorrecto,'
        mensaje += ' debe ser indicado con un número (indicando la cantidad)'

        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control input-form'}),
            'anio_ejercicio_fiscal': NumberInput(attrs={
                'class': 'form-control input-form'}),
            'recurso_asignado': NumberInput(attrs={'class': 'form-control input-form', 'oninput':"edValueKeyPress()"}),
            'fuente': TextInput(attrs={'class': 'form-control input-form'}),
            'capitulo': TextInput(attrs={'class': 'form-control input-form'}),
            'status': Select(attrs={'class': 'form-control input-form'}),
            'tipo_programa_p': Select(attrs={'class': 'form-control input-form'}),
        }

        error_messages = {
            'nombre': {'max_length': LONGITUD_MAXIMA,
                       'required': 'El nombre del programa es requerido,'
                       +' favor de especificarlo.'},
            'anio_ejercicio_fiscal': {'invalid': FORMATO_NUMERO_INCORRECTO,
                                      'required': FORMATO_NUMERO_INCORRECTO},
            'recurso_asignado': {'max_digits': mensaje,
                                 'required':'El recurso estatal asignado es requerido,'
                        + ' favor de indicarlo.'},
            'fuente': {'required':
                        'La fuente del recurso es requerida,'
                        + ' favor de indicarla.'},
            'capitulo': {'required':
                        'El capítulo es requerido,'
                        + ' favor de indicarlo.'}  
        }

    def save(self, commit=True):
        programa = super(ProgramaForm, self).save(commit=False)
        if commit:
            programa.save()
        return programa

# Pendiente Pruebas


class PartidaForm(ModelForm):

    class Meta:
        model = Partida
        exclude = ['programa']

        widgets = {
            'numero_partida': NumberInput(attrs={'class': 'form-control'}),
            'nombre_partida': TextInput(attrs={'class': 'form-control'}),
            'monto_partida': NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        partida = super(PartidaForm, self).save(commit=False)
        if commit:
            partida.save()
        return partida

# Pendiente el de los modelos de Meta

class InversionForm(ModelForm):
    class Meta:
        model = Inversion
        exclude = ['programa_inversion']

        widgets = {
            'recurso_internacional': NumberInput(attrs={'class': 'form-control input-form'}),
            'recurso_federal': NumberInput(attrs={
                                                'class': 'form-control input-form'}),
            'recurso_estatal': NumberInput(attrs={'class': 'form-control input-form'}),
            'recurso_municipal': NumberInput(attrs={'class': 'form-control input-form'}),
            'beneficiario': TextInput(attrs={'class': 'form-control input-form'}),
            'inversion_total': NumberInput(attrs={'class': 'form-control input-form', 'readonly':'readonly'}),
        }
        error_messages = {
            'recurso_internacional' : {
                'required': 'El recurso internacional es requerido,'
                        + ' favor de indicarlo.'},
            'recurso_federal' : {'required':
                        'El recurso federal es requerido,'
                        + ' favor de indicarlo.'},
            'recurso_estatal' : {'required':
                        'El recurso estatal es requerido,'
                        + ' favor de indicarlo.'},
            'recurso_municipal' : {'required':
                        'El recurso municipal es requerido,'
                        + ' favor de indicarlo.'},
            'beneficiario' : {'required':
                        'El nombre del beneficiario es requerido,'
                        + ' favor de indicarlo.'},
            'inversion_total' : {'required':
                        'La inversión total es requerida,'
                        + ' favor de indicarla.'}
        }

    def save(self, commit=True):
        inversion = super(InversionForm, self).save(commit=False)
        if commit:
            inversion.save()
        return inversion

    def clean_inversion_total(self, **kwargs):
        suma_inversion_total = 0
        rec_internacional = float(self.data['recurso_internacional'])
        rec_federal = float(self.data['recurso_federal'])
        rec_estatal = float(self.data['recurso_estatal'])
        rec_municipal = float(self.data['recurso_municipal'])
        suma_inversion_total = rec_internacional + rec_federal + rec_estatal + rec_municipal
        print(self.data['inversion_total'])
        print(suma_inversion_total)
        if float(self.data['inversion_total']) != suma_inversion_total:
            raise ValidationError("La sumatoria total no corresponde con la esperada.")
        return self.data['inversion_total'] 


class MetaForm(ModelForm):
    class Meta:
        model = MetaPrograma
        exclude = ['programa', 'meta_esperada']

        widgets = {
            'numero_actividades': NumberInput(attrs={'class': 'form-control input-form'}),
            'numero_beneficiarios': NumberInput(attrs={
                                                'class': 'form-control input-form'}),
            'numero_hombres': NumberInput(attrs={'class': 'form-control input-form'}),
            'numero_mujeres': NumberInput(attrs={'class': 'form-control input-form'}),
            'edad': Select(attrs={'class': 'form-control input-form'}),
        }

        error_messages = {
            'numero_actividades' : {
                'required': 'El número de actividades es requerido,'
                        + ' favor de indicarlo.'},
            'numero_beneficiarios' : {
                'required': 'El número de beneficiarios es requerido,'
                        + ' favor de indicarlo.'},
            'numero_hombres' : {
                'required': 'El número de hombres es requerido,'
                        + ' favor de indicarlo.'},
            'numero_mujeres' : {
                'required': 'El número de mujeres es requerido,'
                        + ' favor de indicarlo.'}
        }

    def save(self, commit=True):
        meta_prog = super(MetaForm, self).save(commit=False)
        if commit:
            meta_prog.save()
        return meta_prog


class MetaRealForm(ModelForm):
    class Meta:
        model = MetaReal
        exclude = ['programa_r', 'meta_esperada_r']

        widgets = {
            'numero_actividades_r': NumberInput(attrs={
                                                'class': 'form-control input-form'}),
            'numero_beneficiarios_r': NumberInput(attrs={
                'class': 'form-control input-form'}),
            'numero_hombres_r': NumberInput(attrs={'class': 'form-control input-form'}),
            'numero_mujeres_r': NumberInput(attrs={'class': 'form-control input-form'}),
            'edad_r': Select(attrs={'class': 'form-control input-form'}),
        }

        error_messages = {
            'numero_actividades_r' : {
                'required': 'El número de actividades es requerido,'
                        + ' favor de indicarlo.'},
            'numero_beneficiarios_r' : {
                'required': 'El número de beneficiarios es requerido,'
                        + ' favor de indicarlo.'},
            'numero_hombres_r' : {
                'required': 'El número de hombres es requerido,'
                        + ' favor de indicarlo.'},
            'numero_mujeres_r' : {
                'required': 'El número de mujeres es requerido,'
                        + ' favor de indicarlo.'}
        }

    def save(self, commit=True):
        meta_real = super(MetaRealForm, self).save(commit=False)
        if commit:
            meta_real.save()
        return meta_real
